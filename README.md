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

<table>
    <thead>
        <tr>
            <th rowspan="2">Model</th>
            <th colspan="3">Case</th>
            <th colspan="3">Moral</th>
            <th colspan="3">Theory</th>
            <th colspan="2">Avg.</th>
            <th colspan="3">Case (QA)</th>
        </tr>
        <tr>
            <th>SMCQ</th>
            <th colspan="2">MMCQ</th>
            <th>SMCQ</th>
            <th colspan="2">MMCQ</th>
            <th>SMCQ</th>
            <th colspan="2">MMCQ</th>
            <th></th>
            <th></th>
            <th>R-1</th>
            <th>R-L</th>
            <th>B-4</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>MiniCPM4-8B</td>
            <td>50.00</td>
            <td>28.59</td>
            <td><u>43.64</u></td>
            <td>81.58</td>
            <td>50.63</td>
            <td><u>58.23</u></td>
            <td>65.62</td>
            <td>34.06</td>
            <td><u>43.00</u></td>
            <td>51.75</td>
            <td>(<u>57.01</u>)</td>
            <td>23.05</td>
            <td>12.90</td>
            <td>1.35</td>
        </tr>
        <tr>
            <td>Qwen2.5-7B-Instruct</td>
            <td>47.57</td>
            <td>31.64</td>
            <td><u>47.49</u></td>
            <td>87.83</td>
            <td>59.50</td>
            <td><u>71.02</u></td>
            <td>78.46</td>
            <td>42.45</td>
            <td><u>55.17</u></td>
            <td>57.91</td>
            <td>(<u>64.59</u>)</td>
            <td>20.94</td>
            <td>11.28</td>
            <td>1.28</td>
        </tr>
        <tr>
            <td>Qwen2.5-14B-Instruct</td>
            <td>47.13</td>
            <td>41.10</td>
            <td><u>55.93</u></td>
            <td>89.81</td>
            <td>63.93</td>
            <td><u>73.60</u></td>
            <td>80.32</td>
            <td>50.16</td>
            <td><u>61.26</u></td>
            <td>62.08</td>
            <td>(<u>68.01</u>)</td>
            <td>22.69</td>
            <td>13.93</td>
            <td>1.53</td>
        </tr>
        <tr>
            <td>Qwen2.5-72B-Instruct</td>
            <td>46.91</td>
            <td>40.34</td>
            <td><u>53.11</u></td>
            <td>90.79</td>
            <td>70.25</td>
            <td><u>78.48</u></td>
            <td>82.63</td>
            <td>47.63</td>
            <td><u>59.74</u></td>
            <td>63.09</td>
            <td>(<u>68.61</u>)</td>
            <td>21.43</td>
            <td>12.02</td>
            <td>1.16</td>
        </tr>
        <tr>
            <td>DeepSeek-R1</td>
            <td><b>79.25</b></td>
            <td>44.25</td>
            <td><u>60.86</u></td>
            <td><b>95.39</b></td>
            <td>68.99</td>
            <td><u>77.95</u></td>
            <td><b>92.19</b></td>
            <td>57.60</td>
            <td><u>69.41</u></td>
            <td>72.95</td>
            <td>(<b><u>79.18</u></b>)</td>
            <td>17.65</td>
            <td>9.19</td>
            <td>0.94</td>
        </tr>
        <tr>
            <td>DeepSeek-R1-70B</td>
            <td>56.30</td>
            <td>30.72</td>
            <td><u>46.95</u></td>
            <td>88.16</td>
            <td>52.53</td>
            <td><u>65.66</u></td>
            <td>68.01</td>
            <td>25.64</td>
            <td><u>45.63</u></td>
            <td>53.56</td>
            <td>(<u>61.79</u>)</td>
            <td>22.77</td>
            <td>13.23</td>
            <td>1.16</td>
        </tr>
        <tr>
            <td>QwQ-32B</td>
            <td>56.51</td>
            <td>23.35</td>
            <td><u>41.27</u></td>
            <td>88.82</td>
            <td>41.14</td>
            <td><u>53.06</u></td>
            <td>82.12</td>
            <td>32.69</td>
            <td><u>49.90</u></td>
            <td>54.11</td>
            <td>(<u>61.95</u>)</td>
            <td>18.39</td>
            <td>7.48</td>
            <td>0.84</td>
        </tr>
        <tr>
            <td>Qwen3-30B-A3B</td>
            <td>59.65</td>
            <td>31.51</td>
            <td><u>47.28</u></td>
            <td>91.45</td>
            <td>55.06</td>
            <td><u>65.66</u></td>
            <td>80.75</td>
            <td>47.45</td>
            <td><u>59.25</u></td>
            <td>60.98</td>
            <td>(<u>67.34</u>)</td>
            <td>20.53</td>
            <td>12.06</td>
            <td>1.18</td>
        </tr>
        <tr>
            <td>Qwen3-235B-A22B</td>
            <td>68.58</td>
            <td>41.91</td>
            <td><u>57.24</u></td>
            <td>93.42</td>
            <td>69.62</td>
            <td><u>78.90</u></td>
            <td>88.36</td>
            <td>56.70</td>
            <td><u>68.64</u></td>
            <td>69.77</td>
            <td>(<u>75.86</u>)</td>
            <td>18.96</td>
            <td>11.14</td>
            <td>1.11</td>
        </tr>
        <tr>
            <td>Magistral-Small-2506</td>
            <td>56.58</td>
            <td>33.26</td>
            <td><u>49.11</u></td>
            <td>82.89</td>
            <td>53.80</td>
            <td><u>67.99</u></td>
            <td>70.10</td>
            <td>37.76</td>
            <td><u>52.35</u></td>
            <td>55.73</td>
            <td>(<u>63.17</u>)</td>
            <td>22.90</td>
            <td>11.97</td>
            <td>1.21</td>
        </tr>
        <tr>
            <td>GPT-4o</td>
            <td>65.63</td>
            <td>13.67</td>
            <td><u>34.53</u></td>
            <td>88.15</td>
            <td>33.54</td>
            <td><u>54.79</u></td>
            <td>74.65</td>
            <td>24.10</td>
            <td><u>45.07</u></td>
            <td>49.96</td>
            <td>(<u>60.47</u>)</td>
            <td>23.45</td>
            <td>12.75</td>
            <td>1.18</td>
        </tr>
        <tr>
            <td>Gemini1.5-Pro-Latest</td>
            <td>61.04</td>
            <td>35.57</td>
            <td><u>49.87</u></td>
            <td>84.87</td>
            <td>62.03</td>
            <td><u>70.62</u></td>
            <td>80.84</td>
            <td>43.22</td>
            <td><u>53.44</u></td>
            <td>61.26</td>
            <td>(<u>66.78</u>)</td>
            <td>21.63</td>
            <td>10.93</td>
            <td>1.06</td>
        </tr>
        <tr>
            <td>Claude3.7-Sonnet</td>
            <td>63.39</td>
            <td>19.40</td>
            <td><u>34.23</u></td>
            <td>90.13</td>
            <td>60.13</td>
            <td><u>70.04</u></td>
            <td>76.73</td>
            <td>37.37</td>
            <td><u>48.99</u></td>
            <td>57.86</td>
            <td>(<u>63.92</u>)</td>
            <td>21.59</td>
            <td>11.11</td>
            <td>1.23</td>
        </tr>
        <tr>
            <td>CPsyCounX</td>
            <td>40.87</td>
            <td>16.91</td>
            <td><u>32.90</u></td>
            <td>75.17</td>
            <td>36.08</td>
            <td><u>54.85</u></td>
            <td>54.78</td>
            <td>19.03</td>
            <td><u>38.90</u></td>
            <td>40.47</td>
            <td>(<u>49.58</u>)</td>
            <td>22.83</td>
            <td>11.94</td>
            <td>1.48</td>
        </tr>
        <tr>
            <td>EmoLLM</td>
            <td>46.93</td>
            <td>21.87</td>
            <td><u>40.02</u></td>
            <td>84.21</td>
            <td>34.17</td>
            <td><u>51.05</u></td>
            <td>71.72</td>
            <td>26.18</td>
            <td><u>44.49</u></td>
            <td>47.51</td>
            <td>(<u>56.40</u>)</td>
            <td>22.15</td>
            <td>11.69</td>
            <td>1.20</td>
        </tr>
        <tr>
            <td>PsycoLLM</td>
            <td>55.58</td>
            <td>35.07</td>
            <td><u>42.89</u></td>
            <td>88.81</td>
            <td>69.62</td>
            <td><u>74.20</u></td>
            <td>72.63</td>
            <td>48.59</td>
            <td><u>54.12</u></td>
            <td>61.72</td>
            <td>(<u>64.71</u>)</td>
            <td>24.45</td>
            <td><b>17.45</b></td>
            <td>2.04</td>
        </tr>
        <tr>
            <td>PsyDT</td>
            <td>35.56</td>
            <td>35.20</td>
            <td><u>50.14</u></td>
            <td>86.33</td>
            <td>69.70</td>
            <td><u>78.66</u></td>
            <td>80.70</td>
            <td>52.72</td>
            <td><u>62.26</u></td>
            <td>60.04</td>
            <td>(<u>65.61</u>)</td>
            <td>20.65</td>
            <td>13.41</td>
            <td>1.16</td>
        </tr>
        <tr>
            <td>Psyche-R1</td>
            <td>63.31</td>
            <td><b>56.26</b></td>
            <td><b><u>66.21</u></b></td>
            <td>92.76</td>
            <td><b>79.62</b></td>
            <td><b><u>82.54</u></b></td>
            <td>87.70</td>
            <td><b>66.54</b></td>
            <td><b><u>73.34</u></b></td>
            <td><b>74.37</b></td>
            <td>(<u>77.64</u>)</td>
            <td><b>27.31</b></td>
            <td>15.33</td>
            <td><b>2.40</b></td>
        </tr>
    </tbody>
</table>

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
