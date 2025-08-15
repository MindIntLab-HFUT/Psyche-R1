# 中文心理推理大模型Psyche-R1
<a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache%202-red.svg"></a><img src="https://img.shields.io/badge/python-3.8+-blue.svg" /><a href='https://arxiv.org/pdf/2508.10848'><img src='https://img.shields.io/badge/ArXiv-2508.10848-red'></a>

Paper here -> [Psyche-R1: Towards Reliable Psychological LLMs through Unified Empathy, Expertise, and Reasoning](https://arxiv.org/pdf/2508.10848)

## 最近更新
🔥[2025.8.16] 中文心理推理大模型Psyche-R1（亦称PsycoLLM-R1）正式发布！如有需要下载模型，请点击此处：[MACLAB-HFUT/Psyche-R1](https://huggingface.co/MACLAB-HFUT/Psyche-R1)

## 简介

自[PsycoLLM](https://github.com/MACLAB-HFUT/PsycoLLM)发布以来，我们始终致力于探索AI+心理健康领域，寻求进一步的提升与突破。

现有的心理大模型，如[EmoLLM](https://github.com/SmartFlowAI/EmoLLM)和[SoulChat](https://github.com/scutcyr/SoulChat)，普遍强调情感支持与陪伴，侧重于提高模型的共情能力。然而，它们往往缺乏扎实的心理学专业知识和复杂的逻辑推理能力，在深入分析和推理上表现欠佳。此外，一些在数学、编程等领域表现出色的推理大模型，侧重纯粹的逻辑推理，而缺乏心理学领域所需的共情和领域知识，导致在心理领域表现不佳。简单来说，就是“共情”、“领域知识”和“推理”很难兼得，这限制了心理大模型的表现。

为此，我们提出了中文心理推理大模型Psyche-R1，首次统一了共情、专业知识和推理能力。

我们提出了一个全新的数据合成管道，如下图所示。通过数据清洗、题目生成、解释迭代和共情对话合成等流程，我们生成了超过7.5万条带有详细心理学解释的心理学题目问答对、以及7.3万条共情对话数据。在此基础上，我们利用多模型的选择，筛选出高难度的“挑战题”，以用于强化模型的复杂推理能力，其余数据则被划分为“非挑战题”。
![Our proposed pipeline for generating high-quality psychology data.](figure/pipeline.png)

模型首先在海量的“非挑战题”（包括心理学题目和共情对话数据）进行SFT，为模型注入广泛的专业知识和共情能力。在此基础上，模型基于“挑战题”进行GRPO强化学习训练，以进一步提高模型的复杂推理能力。

在多个权威的心理学基准测试中，仅有7B参数的Psyche-R1，其表现不仅显著超越其他同等规模的模型，甚至与671B参数的DeepSeek-R1表现相当。无论是在选择题还是开放式问答中，Psyche-R1都展现出了卓越的心理学领域能力。

## 致谢

模型训练基于[LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)和[VeRL](https://github.com/volcengine/verl)框架进行。

同时，感谢以下同学对本项目的帮助，包括但不限于数据收集、数据处理等（排名不分先后）：邓宇航、金逸多、李想、刘悦、罗妍、王卫东、禹锦明

## 引用

If this work is helpful, please kindly cite as:

```bibtex
@misc{dai2025psycher1reliablepsychologicalllms,
      title={Psyche-R1: Towards Reliable Psychological LLMs through Unified Empathy, Expertise, and Reasoning}, 
      author={Chongyuan Dai and Jinpeng Hu and Hongchang Shi and Zhuo Li and Xun Yang and Meng Wang},
      year={2025},
      eprint={2508.10848},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2508.10848}, 
}
```
