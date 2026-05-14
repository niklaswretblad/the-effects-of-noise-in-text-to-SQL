import os
import sqlite3
import logging
from collections import Counter

from src.timer import Timer
from src.utils import load_json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS_DIR = os.path.join(REPO_ROOT, "datasets")


class Dataset:
    DB_PATH = os.path.join(DATASETS_DIR, "financial.sqlite")
    DB_DESCRIPTIONS_PATH = os.path.join(DATASETS_DIR, "database_description")

    def __init__(self, data_path):
        self.data_path = data_path
        self.conn = None
        self.cursor = None
        self.data = []
        self.total_predicted_execution_time = 0
        self.total_gold_execution_time = 0
        self.last_predicted_execution_time = 0
        self.last_gold_execution_time = 0
        self.current_database_schema = ""

        self.load_data()
        self.load_db()

    def load_data(self):
        self.data = load_json(self.data_path)

    def load_db(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cursor = self.conn.cursor()

    def get_number_of_data_points(self):
        return len(self.data)

    def get_data_point(self, index):
        return self.data[index]

    def execute_queries_and_match_data(self, sql, gold_sql):
        """Execute the predicted and gold SQL and return 1 if results match, else 0."""
        try:
            with Timer() as t:
                self.cursor.execute(sql)
                pred_res = self.cursor.fetchall()

            if t.elapsed_time > 5:
                logging.info(f"Predicted query execution time: {t.elapsed_time:.2f} \nSQL Query:\n" + sql)
            else:
                logging.info(f"Predicted query execution time: {t.elapsed_time:.2f}")

            self.last_predicted_execution_time = t.elapsed_time
            self.total_predicted_execution_time += t.elapsed_time

        except sqlite3.Error as err:
            logging.error("Dataset.execute_queries_and_match_data() " + str(err))
            return 0

        with Timer() as t:
            self.cursor.execute(gold_sql)
            golden_res = self.cursor.fetchall()

        if t.elapsed_time > 5:
            logging.info(f"Golden query execution time: {t.elapsed_time:.2f} \nSQL Query:\n" + gold_sql)
        else:
            logging.info(f"Golden query execution time: {t.elapsed_time:.2f}")

        self.last_gold_execution_time = t.elapsed_time
        self.total_gold_execution_time += t.elapsed_time

        return int(Counter(pred_res) == Counter(golden_res))

    def get_create_table_statements(self):
        self.cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        create_statements = self.cursor.fetchall()
        self.current_database_schema = "\n".join(statement[0] for statement in create_statements)
        return self.current_database_schema

    def get_schema_and_sample_data(self):
        """Return CREATE statements plus three sample rows per table."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in self.cursor.fetchall()]

        sections = []
        for table in tables:
            self.cursor.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table,)
            )
            create_statement = self.cursor.fetchone()[0]

            self.cursor.execute(f'SELECT * FROM "{table}" LIMIT 3;')
            rows = self.cursor.fetchall()

            self.cursor.execute(f'PRAGMA table_info("{table}");')
            column_names = [column[1] for column in self.cursor.fetchall()]

            section = [f"{create_statement};", "", f"Three rows from {table} table:", "\t".join(column_names)]
            for row in rows:
                section.append("\t".join(str(value) for value in row))
            sections.append("\n".join(section))

        self.current_database_schema = "\n\n".join(sections) + "\n"
        return self.current_database_schema

    def get_bird_table_info(self):
        """Concatenate per-table column descriptions from the BIRD CSV files."""
        parts = []
        for filename in sorted(os.listdir(self.DB_DESCRIPTIONS_PATH)):
            if not filename.endswith(".csv"):
                continue
            table_name = filename[:-len(".csv")]
            csv_path = os.path.join(self.DB_DESCRIPTIONS_PATH, filename)
            with open(csv_path, mode="r", encoding="utf-8") as f:
                parts.append(f"Table {table_name}\n{f.read()}")
        return "\n\n".join(parts)


DATASET_LOADERS = {
    "financial": lambda: Dataset(os.path.join(DATASETS_DIR, "financial.json")),
    "financial_corrected": lambda: Dataset(os.path.join(DATASETS_DIR, "financial_corrected.json")),
    "financial_corrected_sql": lambda: Dataset(os.path.join(DATASETS_DIR, "financial_corrected_sql.json")),
}


def get_dataset(dataset_name):
    if dataset_name not in DATASET_LOADERS:
        raise ValueError(
            f"Dataset named '{dataset_name}' not found. "
            f"Available: {sorted(DATASET_LOADERS)}"
        )
    return DATASET_LOADERS[dataset_name]()
