import pandas as pd
import tempfile
import os

def main(inputs: dict, context):
  data = pd.read_csv(inputs["csv"])
  
  return {
    "dataframe": data
  }
