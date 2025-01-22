from oocana import Context
import pandas as pd
import os

def main(params: dict, context: Context):

  data: pd.DataFrame = params["disaster"]

  data.to_csv(os.path.join(params["dir"], params["name"] + ".csv"), index=False)
  
  context.done()
