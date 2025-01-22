from oocana import Context
import pandas as pd

def main(params: dict, context: Context):
  data = pd.read_csv(params["csv"])
  
  return {
    "dataframe": data
  }
