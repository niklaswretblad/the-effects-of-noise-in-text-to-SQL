![](figures/model_results.png?raw=true)

# Understanding the effects of noise in text-to-SQL: An Examination of the BIRD-Bench Benchmark

This is the official repository for the paper ["Understanding the Effects of Noise in Text-to-SQL: An Examination of the BIRD-Bench Benchmark"](https://arxiv.org/abs/2402.12243).

## Datasets

As part of the study, we curate three different datasets which can all be found in the `/datasets` folder: 

1. `financial.json` The original financial domain of BIRD-Bench, which consists of 106 question and SQL query pairs. 
2. `financial_corrected.json` A version of the financial domain where noise has been removed from both questions and SQL queries
3. `financial_corrected_sql.json` A version of the financial domain where only noise in the SQL queries has been removed

## Annotations

On it's way... 

## Prerequisites



## Running the code

This directory contains implementations of the zero-shot model and the DIN-SQL model used in the experiments. For the MAC-SQL model, we instead refer to the projects own repository which can be found [here](https://github.com/wbbeyourself/MAC-SQL), and the datasets found in the `/datasets` folder.

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
