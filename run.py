import os
import json
import torch
import logging
import deepspeed
import torch.distributed as dist

from pathlib import Path
from prompt_toolkit import prompt
from typing import Optional, Dict, List
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import (login, HfFolder, snapshot_download,)



class PsycheR1Chat:
    def __init__(
        self,
        model_name: str = "MindIntLab-HFUT/Psyche-R1",
        model_path: Optional[str] = None,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        max_new_tokens: int = 2048, 
        temperature: float = 0.7,
        top_p: float = 0.9,
        use_auth_token: Optional[str] = None,
        cache_dir: Optional[str] = None,
        local_rank: int = -1
    ):
        self.device = device
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.model_name = model_name
        self.model_path = model_path
        self.cache_dir = cache_dir or Path.home() / '.cache' / 'huggingface'
        self.local_rank = local_rank
        
        self.messages: List[Dict[str, str]] = []
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self._setup_auth(use_auth_token)
        self._setup_distributed()
        self._load_model_and_tokenizer()
    
    def _setup_distributed(self):
        if self.local_rank == -1:
            self.world_size = 1
            return

        deepspeed.init_distributed()
        torch.cuda.set_device(self.local_rank)
        self.world_size = torch.distributed.get_world_size()
        self.logger.info(f"The distributed environment is set up. Local process number: {self.local_rank}, total number of processes: {self.world_size}")
    
    def _setup_auth(self, use_auth_token: Optional[str]):

        if use_auth_token:
            login(token=use_auth_token)
            self.auth_token = use_auth_token
        elif os.getenv("HUGGINGFACE_TOKEN"):
            login(token=os.getenv("HUGGINGFACE_TOKEN"))
            self.auth_token = os.getenv("HUGGINGFACE_TOKEN")
        elif HfFolder.get_token():
            self.auth_token = HfFolder.get_token()
        else:
            self.logger.warning(
                "The HuggingFace authentication token was not provided. Please provide your token if you want to access private models."
            )
            self.auth_token = None
    
    def _load_model_and_tokenizer(self):

        try:
            if self.model_path and os.path.exists(self.model_path):
                self.logger.info(f"Loading model from local path: {self.model_path}...")
                model_path = self.model_path
            else:
                self.logger.info(f"Downloading model from HuggingFace {self.model_name}...")
                model_path = snapshot_download(
                    repo_id=self.model_name,
                    token=self.auth_token,
                    cache_dir=self.cache_dir,
                    local_files_only=False
                )

            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True,
                token=self.auth_token if not self.model_path else None
            )

            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                trust_remote_code=True,
                torch_dtype=torch.float16,
                token=self.auth_token if not self.model_path else None
            )
            
            model.eval()
            
            # DeepSpeed configs
            ds_inference_config = {
                "tensor_parallel": {
                    "tp_size": self.world_size
                },
                "dtype": "fp16",
                "replace_method": "auto",
                "replace_with_kernel_inject": True
            }
            
            self.logger.info(f"Current GPU: {self.local_rank}, total number of processes: {self.world_size}")
            self.logger.info(f"DeepSpeed configs: {ds_inference_config}")
            
            self.model = deepspeed.init_inference(
                model=model,
                config=ds_inference_config
            )
            
            self.logger.info(f"Model loaded successfully! Current process number: {self.local_rank}, total number of processes: {self.world_size}")
            
        except Exception as e:
            self.logger.error(f"Model loading failed: {str(e)}")
            raise

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, str]:
        # Update message history
        if system_prompt and not self.messages:
            self.messages.append({"role": "system", "content": system_prompt})
        self.messages.append({"role": "user", "content": prompt})
        
        try:
            # Formatting conversation history using message templates
            text = self.tokenizer.apply_chat_template(
                self.messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            input_ids = self.tokenizer.encode(text, return_tensors="pt")
            
            if self.local_rank != -1:
                input_ids = input_ids.to(f"cuda:{self.local_rank}")
            else:
                input_ids = input_ids.to(self.device)
            
            # generate responses
            with torch.no_grad():
                outputs = self.model.module.generate(
                    input_ids,
                    max_new_tokens=self.max_new_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id, 
                    **kwargs
                )
            
            new_tokens = outputs[0][len(input_ids[0]):]
            response = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
            
            self.messages.append({"role": "assistant", "content": response})
            
            return {"response": response}

        except Exception as e:
            self.logger.error(f"An error occurred while generating the response: {str(e)}")
            self.messages.pop()
            return {"error": str(e)}
    
    def chat(self, system_prompt: Optional[str] = None):
        if self.local_rank in [-1, 0]:
            print("Welcome to Psyche-R1, the Chinese psychological reasoning LLM! Type 'quit' or 'exit' to end the conversation.")
            if system_prompt:
                print(f"\nSystem prompt: {system_prompt}\n")
            
            while True:
                try:
                    user_input = prompt("\nUser: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\n\nThanks for using the Chinese psychological reasoning LLM Psyche-R1. Goodbye!")
                    break

                if user_input.lower() in ['quit', 'exit']:
                    print("\nThanks for using the Chinese psychological reasoning LLM Psyche-R1. Goodbye!")
                    break
                
                add_prefix_prompt = (
                    # Chinese version
                    "你必须在<think>和</think>标签内给出你的推理过程，然后，在</think>标签后给出最终的答案。"
                    f"\n\n以下是我的问题：\n{user_input}"
                    # English version
                    # "You need to provide your reasoning process within <think> and </think> tags, and then give your answer after the </think> tag."
                    # f"\n\nHere is my question:\n{user_input}"
                )
                    
                try:
                    response = self.generate_response(
                        add_prefix_prompt,
                        system_prompt=system_prompt if not self.messages else None
                    )
                    if "error" in response:
                        print(f"\nError: {response['error']}")
                    else:
                        print("\nAssistant:", response["response"])
                except Exception as e:
                    print(f"\nError occurred: {str(e)}")
                    continue

    def clear_history(self):
        self.messages = []
        self.logger.info("Conversation history cleared.")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--local_rank", type=int, default=-1)
    args = parser.parse_args()
    
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    try:
        chat_bot = PsycheR1Chat(
            model_path="MindIntLab/Psyche-R1", # this is your model path
            cache_dir="./model_cache",
            local_rank=args.local_rank
        )

        # prompt 1: Chinese version
        system_prompt = "你是一名心理学专家。请回答以下心理学案例题目，请逐步思考，仔细分析给定的心理学案例，首先给出你的推理过程，以及得出该推理结论的详细解释和事实理由，解释你是从什么事实中得出结论的，然后给出答案。注意，推理过程需要包含在 <think> 和 </think> 之间。"
        # prompt 1: English version
        # system_prompt = "You are an expert in psychology. Please answer the following psychologicy case questions. Then, let's think step by step and carefully analyze the given psychology case. First, you need to provide your reasoning process along with detailed rationales and factual reasons for reaching that reasoning conclusion. Explain what facts led you to your conclusions, then provide your answer. Note that the reasoning process should be included within <think> and </think> tags."
        
        # prompt 2: Chinese version
        # system_prompt = "你是一名心理学专家，具有丰富的理论知识和工作经验。你需要首先阅读以下心理学问题，然后，请逐步思考，运用心理学知识进行分析和推理。你必须在<think>和</think>标签内给出你的推理过程，然后，在</think>标签后给出最终的答案。"
        # prompt 2: English version
        # system_prompt = "You are an expert in psychology with extensive theoretical knowledge and work experience. First, you need to read the following psychology questions. Then, let's think step by step, applying your psychology knowledge for analysis and reasoning. You need to provide your reasoning process within <think> and </think> tags, and then give your answer after the </think> tag."
        
        chat_bot.chat(system_prompt=system_prompt)
        
    except Exception as e:
        print(f"An error occurred while launching Psyche-R1: {str(e)}")

if __name__ == "__main__":
    main()
