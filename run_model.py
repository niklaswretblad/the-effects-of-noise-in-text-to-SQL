import argparse
import os
import json
import logging
from datetime import datetime

from langchain.chat_models import ChatOpenAI

from src.datasets import get_dataset, DATASET_LOADERS
from src.models.zero_shot import ZeroShotModel
from src.models.din_sql import DinSQLModel


AVAILABLE_MODELS = ("zero_shot", "din_sql")

log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename="debug.log", level=logging.DEBUG, format=log_format)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def build_model(model_name, llm):
    if model_name == "zero_shot":
        return ZeroShotModel(llm)
    if model_name == "din_sql":
        return DinSQLModel(llm)
    raise ValueError(f"Unknown model '{model_name}'. Available: {AVAILABLE_MODELS}")


def run_model_on_dataset(model_name, dataset_name, llm_name):
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    dataset = get_dataset(dataset_name)

    llm = ChatOpenAI(
        openai_api_key=api_key,
        model_name=llm_name,
        temperature=0,
        request_timeout=60,
    )

    model = build_model(model_name, llm)

    if model_name == "zero_shot":
        sql_schema = dataset.get_create_table_statements()
        bird_table_info = None
    else:
        sql_schema = dataset.get_schema_and_sample_data()
        bird_table_info = dataset.get_bird_table_info()

    no_data_points = dataset.get_number_of_data_points()
    score = 0
    accuracy = 0.0
    results = []

    for i in range(no_data_points):
        data_point = dataset.get_data_point(i)
        evidence = data_point["evidence"]
        golden_sql = data_point["SQL"]
        db_id = data_point["db_id"]
        question = data_point["question"]
        difficulty = data_point.get("difficulty", "")

        if model_name == "zero_shot":
            predicted_sql = model.generate_query(sql_schema, question, evidence)
        else:
            predicted_sql = model.generate_query(sql_schema, bird_table_info, evidence, question)

        success = dataset.execute_queries_and_match_data(predicted_sql, golden_sql)

        score += success
        accuracy = score / (i + 1)

        results.append({
            "Question": question,
            "Gold Query": golden_sql,
            "Predicted Query": predicted_sql,
            "Success": success,
            "Difficulty": difficulty,
        })

        print(
            f"Percentage done: {round((i + 1) / no_data_points * 100, 2)}% "
            f"Domain: {db_id} Success: {success} Accuracy: {accuracy:.4f}"
        )

    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(logs_dir, f"results_{timestamp}.json")

    with open(filepath, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Total Accuracy: {accuracy:.4f}")
    print(f"Results logged in {filepath}")


def main():
    parser = argparse.ArgumentParser(
        description="Run text-to-SQL models on the BIRD-Bench financial datasets."
    )
    parser.add_argument(
        "--model", type=str, default="zero_shot", choices=AVAILABLE_MODELS,
        help="Which model to run.",
    )
    parser.add_argument(
        "--dataset", type=str, default="financial", choices=sorted(DATASET_LOADERS),
        help="Which dataset variant to evaluate on.",
    )
    parser.add_argument(
        "--llm", type=str, default="gpt-3.5-turbo",
        help="OpenAI chat model id (e.g. gpt-3.5-turbo, gpt-4).",
    )

    args = parser.parse_args()
    run_model_on_dataset(args.model, args.dataset, args.llm)


if __name__ == "__main__":
    main()
