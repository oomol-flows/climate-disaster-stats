import pandas as pd
import os

def main(inputs: dict, context):

  data: pd.DataFrame = inputs["disaster"]

  data.to_csv(os.path.join(inputs["dir"], inputs["name"] + ".csv"), index=False)
  
  context.done()
