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

我们随后进行了详细的评估实验。在多个权威的心理学基准测试中，仅有7B参数的Psyche-R1，其表现不仅显著超越其他同等规模的模型，甚至与671B参数的DeepSeek-R1表现相当。

模型在 [Psychological Counselor Examination Benchmark (PCEB)](https://github.com/MACLAB-HFUT/PsycoLLM)的实验结果如下。注意，我们仅展示了部分的实验结果，完整实验结果请看文章。其中，下划线数字表示 MMCQ 的弹性正确率，粗体数字表示该项中的最佳性能，平均值表示严格正确率的平均值，括号内的值表示 SMCQ 的严格正确率和 MMCQ 的弹性正确率的平均值。实验结果表明，无论是在选择题还是开放式问答中，Psyche-R1都展现出了卓越的心理学领域能力。
<table>
    <thead>
        <tr>
            <th rowspan="2" align="left">Model</th>
            <th colspan="3" align="center">Case</th>
            <th colspan="3" align="center">Moral</th>
            <th colspan="3" align="center">Theory</th>
            <th rowspan="2" colspan="2" align="center">Avg.</th>
            <th colspan="3" align="center">Case (QA)</th>
        </tr>
        <tr>
            <th align="center">SMCQ</th>
            <th colspan="2" align="center">MMCQ</th>
            <th align="center">SMCQ</th>
            <th colspan="2" align="center">MMCQ</th>
            <th align="center">SMCQ</th>
            <th colspan="2" align="center">MMCQ</th>
            <th align="center">R-1</th>
            <th align="center">R-L</th>
            <th align="center">B-4</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left">MiniCPM4-8B</td>
            <td align="center">50.00</td>
            <td align="center">28.59</td>
            <td align="center"><u>43.64</u></td>
            <td align="center">81.58</td>
            <td align="center">50.63</td>
            <td align="center"><u>58.23</u></td>
            <td align="center">65.62</td>
            <td align="center">34.06</td>
            <td align="center"><u>43.00</u></td>
            <td align="center">51.75</td>
            <td align="center">(<u>57.01</u>)</td>
            <td align="center">23.05</td>
            <td align="center">12.90</td>
            <td align="center">1.35</td>
        </tr>
        <tr>
            <td align="left">Qwen2.5-7B-Instruct</td>
            <td align="center">47.57</td>
            <td align="center">31.64</td>
            <td align="center"><u>47.49</u></td>
            <td align="center">87.83</td>
            <td align="center">59.50</td>
            <td align="center"><u>71.02</u></td>
            <td align="center">78.46</td>
            <td align="center">42.45</td>
            <td align="center"><u>55.17</u></td>
            <td align="center">57.91</td>
            <td align="center">(<u>64.59</u>)</td>
            <td align="center">20.94</td>
            <td align="center">11.28</td>
            <td align="center">1.28</td>
        </tr>
        <tr>
            <td align="left">Qwen2.5-72B-Instruct</td>
            <td align="center">46.91</td>
            <td align="center">40.34</td>
            <td align="center"><u>53.11</u></td>
            <td align="center">90.79</td>
            <td align="center">70.25</td>
            <td align="center"><u>78.48</u></td>
            <td align="center">82.63</td>
            <td align="center">47.63</td>
            <td align="center"><u>59.74</u></td>
            <td align="center">63.09</td>
            <td align="center">(<u>68.61</u>)</td>
            <td align="center">21.43</td>
            <td align="center">12.02</td>
            <td align="center">1.16</td>
        </tr>
        <tr>
            <td align="left">DeepSeek-R1</td>
            <td align="center"><b>79.25</b></td>
            <td align="center">44.25</td>
            <td align="center"><u>60.86</u></td>
            <td align="center"><b>95.39</b></td>
            <td align="center">68.99</td>
            <td align="center"><u>77.95</u></td>
            <td align="center"><b>92.19</b></td>
            <td align="center">57.60</td>
            <td align="center"><u>69.41</u></td>
            <td align="center">72.95</td>
            <td align="center">(<b><u>79.18</u></b>)</td>
            <td align="center">17.65</td>
            <td align="center">9.19</td>
            <td align="center">0.94</td>
        </tr>
        <tr>
            <td align="left">DeepSeek-R1-70B</td>
            <td align="center">56.30</td>
            <td align="center">30.72</td>
            <td align="center"><u>46.95</u></td>
            <td align="center">88.16</td>
            <td align="center">52.53</td>
            <td align="center"><u>65.66</u></td>
            <td align="center">68.01</td>
            <td align="center">25.64</td>
            <td align="center"><u>45.63</u></td>
            <td align="center">53.56</td>
            <td align="center">(<u>61.79</u>)</td>
            <td align="center">22.77</td>
            <td align="center">13.23</td>
            <td align="center">1.16</td>
        </tr>
        <tr>
            <td align="left">QwQ-32B</td>
            <td align="center">56.51</td>
            <td align="center">23.35</td>
            <td align="center"><u>41.27</u></td>
            <td align="center">88.82</td>
            <td align="center">41.14</td>
            <td align="center"><u>53.06</u></td>
            <td align="center">82.12</td>
            <td align="center">32.69</td>
            <td align="center"><u>49.90</u></td>
            <td align="center">54.11</td>
            <td align="center">(<u>61.95</u>)</td>
            <td align="center">18.39</td>
            <td align="center">7.48</td>
            <td align="center">0.84</td>
        </tr>
        <tr>
            <td align="left">Qwen3-235B-A22B</td>
            <td align="center">68.58</td>
            <td align="center">41.91</td>
            <td align="center"><u>57.24</u></td>
            <td align="center">93.42</td>
            <td align="center">69.62</td>
            <td align="center"><u>78.90</u></td>
            <td align="center">88.36</td>
            <td align="center">56.70</td>
            <td align="center"><u>68.64</u></td>
            <td align="center">69.77</td>
            <td align="center">(<u>75.86</u>)</td>
            <td align="center">18.96</td>
            <td align="center">11.14</td>
            <td align="center">1.11</td>
        </tr>
        <tr>
            <td align="left">Magistral-Small-2506</td>
            <td align="center">56.58</td>
            <td align="center">33.26</td>
            <td align="center"><u>49.11</u></td>
            <td align="center">82.89</td>
            <td align="center">53.80</td>
            <td align="center"><u>67.99</u></td>
            <td align="center">70.10</td>
            <td align="center">37.76</td>
            <td align="center"><u>52.35</u></td>
            <td align="center">55.73</td>
            <td align="center">(<u>63.17</u>)</td>
            <td align="center">22.90</td>
            <td align="center">11.97</td>
            <td align="center">1.21</td>
        </tr>
        <tr>
            <td align="left">GPT-4o</td>
            <td align="center">65.63</td>
            <td align="center">13.67</td>
            <td align="center"><u>34.53</u></td>
            <td align="center">88.15</td>
            <td align="center">33.54</td>
            <td align="center"><u>54.79</u></td>
            <td align="center">74.65</td>
            <td align="center">24.10</td>
            <td align="center"><u>45.07</u></td>
            <td align="center">49.96</td>
            <td align="center">(<u>60.47</u>)</td>
            <td align="center">23.45</td>
            <td align="center">12.75</td>
            <td align="center">1.18</td>
        </tr>
        <tr>
            <td align="left">Gemini1.5-Pro-Latest</td>
            <td align="center">61.04</td>
            <td align="center">35.57</td>
            <td align="center"><u>49.87</u></td>
            <td align="center">84.87</td>
            <td align="center">62.03</td>
            <td align="center"><u>70.62</u></td>
            <td align="center">80.84</td>
            <td align="center">43.22</td>
            <td align="center"><u>53.44</u></td>
            <td align="center">61.26</td>
            <td align="center">(<u>66.78</u>)</td>
            <td align="center">21.63</td>
            <td align="center">10.93</td>
            <td align="center">1.06</td>
        </tr>
        <tr>
            <td align="left">Claude3.7-Sonnet</td>
            <td align="center">63.39</td>
            <td align="center">19.40</td>
            <td align="center"><u>34.23</u></td>
            <td align="center">90.13</td>
            <td align="center">60.13</td>
            <td align="center"><u>70.04</u></td>
            <td align="center">76.73</td>
            <td align="center">37.37</td>
            <td align="center"><u>48.99</u></td>
            <td align="center">57.86</td>
            <td align="center">(<u>63.92</u>)</td>
            <td align="center">21.59</td>
            <td align="center">11.11</td>
            <td align="center">1.23</td>
        </tr>
        <tr>
            <td align="left">EmoLLM</td>
            <td align="center">46.93</td>
            <td align="center">21.87</td>
            <td align="center"><u>40.02</u></td>
            <td align="center">84.21</td>
            <td align="center">34.17</td>
            <td align="center"><u>51.05</u></td>
            <td align="center">71.72</td>
            <td align="center">26.18</td>
            <td align="center"><u>44.49</u></td>
            <td align="center">47.51</td>
            <td align="center">(<u>56.40</u>)</td>
            <td align="center">22.15</td>
            <td align="center">11.69</td>
            <td align="center">1.20</td>
        </tr>
        <tr>
            <td align="left">PsycoLLM</td>
            <td align="center">55.58</td>
            <td align="center">35.07</td>
            <td align="center"><u>42.89</u></td>
            <td align="center">88.81</td>
            <td align="center">69.62</td>
            <td align="center"><u>74.20</u></td>
            <td align="center">72.63</td>
            <td align="center">48.59</td>
            <td align="center"><u>54.12</u></td>
            <td align="center">61.72</td>
            <td align="center">(<u>64.71</u>)</td>
            <td align="center">24.45</td>
            <td align="center"><b>17.45</b></td>
            <td align="center">2.04</td>
        </tr>
        <tr>
            <td align="left">PsyDT</td>
            <td align="center">35.56</td>
            <td align="center">35.20</td>
            <td align="center"><u>50.14</u></td>
            <td align="center">86.33</td>
            <td align="center">69.70</td>
            <td align="center"><u>78.66</u></td>
            <td align="center">80.70</td>
            <td align="center">52.72</td>
            <td align="center"><u>62.26</u></td>
            <td align="center">60.04</td>
            <td align="center">(<u>65.61</u>)</td>
            <td align="center">20.65</td>
            <td align="center">13.41</td>
            <td align="center">1.16</td>
        </tr>
        <tr>
            <td align="left">Psyche-R1</td>
            <td align="center">63.31</td>
            <td align="center"><b>56.26</b></td>
            <td align="center"><b><u>66.21</u></b></td>
            <td align="center">92.76</td>
            <td align="center"><b>79.62</b></td>
            <td align="center"><b><u>82.54</u></b></td>
            <td align="center">87.70</td>
            <td align="center"><b>66.54</b></td>
            <td align="center"><b><u>73.34</u></b></td>
            <td align="center"><b>74.37</b></td>
            <td align="center">(<u>77.64</u>)</td>
            <td align="center"><b>27.31</b></td>
            <td align="center">15.33</td>
            <td align="center"><b>2.40</b></td>
        </tr>
    </tbody>
</table>

<br>

我们还进行了更详细、更全面的实验，包括[CPsyExam](https://aclanthology.org/anthology-files/anthology-files/pdf/coling/2025.coling-main.745.pdf)和[PsyDT](https://arxiv.org/pdf/2412.13660)。

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
