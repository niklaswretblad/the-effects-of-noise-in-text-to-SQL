![](figures/model_results.png?raw=true)

# Understanding the effects of noise in text-to-SQL: An Examination of the BIRD-Bench Benchmark
Code for the paper "Understanding the Effects of Noise in Text-to-SQL: An Examination of the BIRD-Bench Benchmark".

## Abstract & Overview

Text-to-SQL, which involves translating natural language into Structured Query Language (SQL), is crucial for enabling broad access to structured databases without  expert knowledge. However, designing models for such tasks is challenging due to numerous factors, including the presence of 'noise,' such as ambiguous questions and syntactical errors. This study provides an in-depth analysis of the distribution and types of noise in the widely used BIRD-Bench benchmark and the impact of noise on models. While BIRD-Bench was created to model dirty and noisy database values, it was not created to contain noise and errors in the questions and gold queries. We found that noise in questions and gold queries are prevalent in the dataset, with varying amounts across domains, and with an uneven distribution between noise types. The presence of incorrect gold SQL queries, which then generate incorrect gold answers, has a significant impact on the benchmark's reliability. Surprisingly, when evaluating models on corrected SQL queries, zero-shot baselines surpassed the performance of state-of-the-art prompting methods. We conclude that informative noise labels and reliable benchmarks are crucial to developing new Text-to-SQL methods that can handle varying types of noise.

## Datasets

As part of the study, we curate three different datasets which can all be found in the `/datasets` folder: 

1. `financial.json` The original financial domain of BIRD-Bench, which consists of 106 question and SQL query pairs. 
2. `financial_corrected.json` A version of the financial domain where noise has been removed from both questions and SQL queries
3. `financial_corrected_sql.json` A version of the financial domain where only noise in the SQL queries has been removed

## Annotations

On it's way... 

## Run Instructions

On it's way... 

## Citation

Bibtex:
```
@misc{wretblad2024understanding,
      title={Understanding the Effects of Noise in Text-to-SQL: An Examination of the BIRD-Bench Benchmark}, 
      author={Niklas Wretblad and Fredrik Gordh Riseby and Rahul Biswas and Amin Ahmadi and Oskar Holmström},
      year={2024},
      eprint={2402.12243},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
