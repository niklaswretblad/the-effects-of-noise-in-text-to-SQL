
import json

def load_json(path):
   with open(path, 'r') as j:
      data = json.loads(j.read())
   return data

