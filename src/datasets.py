
import sqlite3
import os
import logging

from src.timer import Timer
from src.utils import load_json
from collections import Counter

class Dataset:
   DB_PATH = "/datasets/financial.sqlite"
   DB_DESCRIPTIONS_PATH = "/datasets/database_description"
   data_path = None

   def __init__(self, data_path='/financial/financial.json'):
      self.conn = None
      self.cursor = None
      self.data = []
      self.data_path = data_path
      self.total_predicted_execution_time = 0
      self.total_gold_execution_time = 0
      self.last_predicted_execution_time = 0
      self.last_gold_execution_time = 0

      self.database_schema_str = ""

      self.load_data()
      self.load_db()
      
      
   def load_data(self):      
      if self.data_path is None:
         raise ValueError("DATA_PATH must be defined")
      self.data = load_json(self.data_path)


   def load_db(self):
      self.conn = sqlite3.connect(self.DB_PATH)
      self.cursor = self.conn.cursor()
         
   
   def get_number_of_data_points(self):
      return len(self.data)
   

   def get_data_point(self, index):      
      return self.data[index]

   
   def execute_queries_and_match_data(self, sql: str, gold_sql):
      """
      Execute provided SQL queries and compare the results.

      Parameters:
         sql (str): The predicted SQL query to execute.
         gold_sql (str): The golden SQL query to compare results.

      Returns:
         int: 1 if the results match, otherwise 0.
      """
      
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
         logging.error("DataLoader.execute_queries_and_match_data() " + str(err))
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

      # logging.debug("Predicted data:")
      # logging.debug(set(pred_res))
      # logging.debug("Gold data:")
      # logging.debug(set(golden_res))

      equal = (Counter(pred_res) == Counter(golden_res))
      return int(equal)  


   def get_create_table_statements(self, db_name):
      self.cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
      create_statements = self.cursor.fetchall()

      self.current_database_schema = '\n'.join([statement[0] for statement in create_statements])
      
      return self.current_database_schema
   

   def get_schema_and_sample_data(self):
      """
      Retrieve and return the schema and sample rows/data from a database.

      Returns:
         str: A formatted string containing schema and sample data.
      """      
      self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
      tables = self.cursor.fetchall()
      
      schema_and_sample_data = ""

      for table in tables:
         table = table[0]  
         self.cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}';")
         create_statement = self.cursor.fetchone()[0]
         
         schema_and_sample_data += f"{create_statement};\n\n"
         
         self.cursor.execute(f"SELECT * FROM \"{table}\" LIMIT 3;")
         rows = self.cursor.fetchall()
                  
         self.cursor.execute(f"PRAGMA table_info(\"{table}\");")
         columns = self.cursor.fetchall()
         column_names = [column[1] for column in columns]
         column_names_line = "\t".join(column_names)
         
         schema_and_sample_data += f"Three rows from {table} table:\n"
         schema_and_sample_data += f"{column_names_line}\n"

         for row in rows:
               row_line = "\t".join([str(value) for value in row])
               schema_and_sample_data += f"{row_line}\n"

         schema_and_sample_data += "\n"

      schema_and_sample_data += "\n"

      self.current_database_schema = schema_and_sample_data
    
      return self.current_database_schema
   

   def get_bird_table_info(self):
      """
      Retrieve the table schema and information 
      from the corresponding bird-bench .csv files.

      :param database_name: str, name of the database
      :return: dict, where keys are table names and values are a string
      containing the table information
      """                  
      table_info = ""
      
      for filename in os.listdir(self.DB_DESCRIPTIONS_PATH):
         if filename.endswith(".csv"):
            table_name = filename.rstrip(".csv")
            csv_path = os.path.join(self.DB_DESCRIPTIONS_PATH, filename)
            
            with open(csv_path, mode='r', encoding='utf-8') as file:
               file_contents = file.read()                                   
            
            table_info += "Table " + table_name + "\n"
            table_info += file_contents
      
         table_info += "\n\n"

      return table_info


DATASET_LOADERS = {
    'Financial': lambda: Dataset(),
    'FinancialCorrected': lambda: Dataset(data_path='/financial/financial_corrected.json'),
    'FinancialCorrectedSQL': lambda: Dataset(data_path='/financial/financial_corrected_sql.json'),
}

def get_dataset(dataset_name):
    if dataset_name not in DATASET_LOADERS:
        raise ValueError(f"Dataset named '{dataset_name}' not found.")
    return DATASET_LOADERS[dataset_name]()