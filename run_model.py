import argparse
import os
import logging 
import datetime
import json

from src.models.zero_shot import ZeroShotModel
from src.models.din_sql import DinSQLModel
from src.datasets import get_dataset
from langchain.chat_models import ChatOpenAI



# Load OpenAI API Key
api_key = os.environ.get('OPENAI_API_KEY')
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Enable logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=log_format)

# Suppress debug logs from OpenAI and requests libraries
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def run_model_on_dataset(model_name, dataset_name, llm_name):
    
    dataset = get_dataset(dataset_name)

    llm = ChatOpenAI(
        openai_api_key=api_key,
        model_name=llm_name,
        temperature=0,
        request_timeout=60
    )

    if model_name == "zero_shot":
        model = ZeroShotModel(llm)
    elif model_name == "din_sql":
        model = DinSQLModel(llm)        
    else: 
        raise ValueError("Supplied model_name not implemented")

    no_data_points = dataset.get_number_of_data_points()
    score = 0
    results = []

    if model_name == "zero_shot":
        sql_schema = dataset.get_create_statements()
        predicted_sql = model.generate_query(sql_schema, question, evidence)
    elif model_name == "din_sql":
        sql_schema = dataset.get_schema_and_sample_data(db_id)
        bird_table_info = dataset.get_bird_db_info(db_id)                

    for i in range(no_data_points):
        data_point = dataset.get_data_point(i)
        evidence = data_point['evidence']
        golden_sql = data_point['SQL']
        db_id = data_point['db_id']
        question = data_point['question']
        difficulty = data_point.get('difficulty', "")

        if model_name == "zero_shot":            
            predicted_sql = model.generate_query(sql_schema, question, evidence)
        elif model_name == "din_sql":       
            predicted_sql = model.generate_query(sql_schema, bird_table_info, evidence, question)

        success = dataset.execute_queries_and_match_data(predicted_sql, golden_sql, db_id)

        score += success
        accuracy = score / (i + 1)

        results.append({
            "Question": question,
            "Gold Query": golden_sql,
            "Predicted Query": predicted_sql,
            "Success": success,
            "Difficulty": difficulty
        })

        print(f"Percentage done: {round(i / no_data_points * 100, 2)}% Domain: {db_id} Success: {success} Accuracy: {accuracy}")

    # Save results to JSON file
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(logs_dir, f"results_{timestamp}.json")

    with open(filepath, 'w') as file:
        json.dump(results, file, indent=4)

    print(f"Total Accuracy: {accuracy}")
    print(f"Results logged in {filepath}")

def main():
    parser = argparse.ArgumentParser(description='Run text-to-SQL models on specified datasets with an option to specify the OpenAI LLM to use.')

    # Set default values for model, dataset, and llm (language model) arguments
    parser.add_argument('--model', type=str, default='default_model_name', help='The name of the model to use (default: default_model_name)')
    parser.add_argument('--dataset', type=str, default='default_dataset_name', help='The name of the dataset to use (default: default_dataset_name)')
    parser.add_argument('--llm', type=str, default='GPT-3.5-Turbo', help='The OpenAI language model to use (default: GPT-3.5-Turbo)')

    args = parser.parse_args()

    # Run the specified model on the specified dataset using the specified LLM
    run_model_on_dataset(args.model, args.dataset, args.llm)

if __name__ == '__main__':
    main()
