![](figures/model_results.png?raw=true)

## Introduction

This is the official repository for the paper ["Understanding the Effects of Noise in Text-to-SQL: An Examination of the BIRD-Bench Benchmark"](https://arxiv.org/abs/2402.12243).

We found that the popular BIRD-Bench text-to-SQL dataset and benchmark contains a lot of noise (both in the questions and gold SQL queries), and investigate the effect of noise on model performance. The presence of incorrect gold SQL queries, which then generate incorrect gold answers, has a significant impact on the benchmark's reliability. Surprisingly, when evaluating models on corrected SQL queries, zero-shot baselines surpassed the performance of state-of-the-art prompting methods as can be seen in the above picture. We conclude that informative noise labels and reliable benchmarks are crucial to developing new Text-to-SQL methods that can handle varying types of noise.

## Datasets

As part of the study, we curate three different datasets which can all be found in the `/datasets` folder based on the found errors and annotations: 

1. `financial.json` The original financial domain of BIRD-Bench, which consists of 106 question and SQL query pairs. 
2. `financial_corrected.json` A version of the financial domain where noise has been removed from both questions and SQL queries
3. `financial_corrected_sql.json` A version of the financial domain where only noise in the SQL queries has been removed

## Annotations

The finalized and between the two annotators agreed annotations and corrections can be found in the `/annotations` folder. There are separate files for the annotations of the 106 data points in the financial domain and the sampled data points from the other domains (california_schools, superhero, thrombosis_prediction, toxicology). 20 data points were sampled from each of those domains. There are an excel version and a csv version of each file, where the csv file displays as a table directly in the github interface for quick viewing. There is also an UML diagram of the database schema of the database from the financial domain to help understanding the corrections and annotations. 

Statistics over the found noise and errors can be seen in the table below. Table 1 contains an overview of the noise found in each domains. The identified errors were further grouped based on similarity and named after the errors’ common properties. The annotated categories can be seen in table 2 below.

#### Table 1: Statistics of the total amount of data points that contains errors and the amount of errors in questions and gold queries across five datasets.

| **Statistic** | **Financial** | **California Schools** | **Superhero** | **Toxicology** | **Thrombosis Prediction** |
|---------------|---------------|------------------------|---------------|----------------|---------------------------|
| Data points with noise | 52/106 (49%) | 9/20 (45%) | 3/20 (15%) | 7/20 (35%) | 8/20 (40%) |
| Noisy questions | 44/106 (41.5%) | 5/20 (25%) | 2/20 (10%) | 6/20 (30%) | 3/20 (15%) |
| Erroneous gold queries | 22/106 (20.7%) | 8/20 (40%) | 1/20 (5%) | 2/20 (10%) | 6/20 (30%) |


#### Table 2: Distribution of different types of noise encountered in the domains.

| **Noise Type** | **Financial** | **California Schools** | **Superhero** | **Toxicology** | **Thrombosis Prediction** |
|----------------|---------------|------------------------|---------------|----------------|---------------------------|
| Spelling/Syntactical Errors | 23 | 2 | 1 | 4 | 2 |
| Vague/Ambiguous Questions | 17 | 1 | 1 | 1 | 1 |
| Incorrect SQL | 22 | 8 | 1 | 2 | 6 |
| Synonyms | 2 | 0 | 0 | 0 | 0 |
| String Capitalization | 7 | 0 | 0 | 0 | 0 |
| Question does not map to DB | 1 | 4 | 1 | 0 | 0 |
| **Total number of errors** | **72** | **15** | **4** | **7** | **9** |



## Prerequisites

Install the dependencies: 

```
pip install -r requirements.txt
```

Set the OPENAI_API_KEY environment variable: 

```
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```


## Running the code

Only implementations of the zero-shot model and the DIN-SQL model used in the experiments can be found in this repository. For the MAC-SQL model, we instead refer to the models own repository which can be found [here](https://github.com/wbbeyourself/MAC-SQL), and the datasets found in the `/datasets` folder.

Use the following command format to run a model:

```
python run_model.py [--model MODEL_NAME] [--dataset DATASET_NAME] [--llm LLM_NAME]
```

- `--model ` sets which of the two models to use. The available options are `zero_shot` and `din_sql`
- `--dataset ` sets which of the datasets to use. The available options are `financial`, `financial_corrected` and `financial_corrected_sql`
- `--llm ` sets which of the openAI LLMs to use. See [here](https://platform.openai.com/docs/models/overview) for the available models. 


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
