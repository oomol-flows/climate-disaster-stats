import pandas as pd
import os

def main(inputs: dict, context):
  # TODO 支持直传 dataframe
  data: pd.DataFrame = pd.read_pickle(inputs["disaster"])

  data.to_csv(os.path.join(inputs["dir"], inputs["name"] + ".csv"), index=False)
  
  context.done()
