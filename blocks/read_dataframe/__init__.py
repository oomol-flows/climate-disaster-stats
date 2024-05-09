import pandas as pd
import tempfile
import os

def main(inputs: dict, context):
  data = pd.read_csv(inputs["csv"])
  
  # TODO 支持直传 dataframe
  pkl = os.path.join(tempfile.gettempdir(), "{}.pkl".format(hash(inputs["csv"])))
  data.to_pickle(pkl)

  # TODO 支持直传 dataframe
  context.output(pkl, "dataframe", True)
