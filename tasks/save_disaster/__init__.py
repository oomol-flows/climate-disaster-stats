from oocana import Context
import pandas as pd
import os

def main(params: dict, context: Context):

  data: pd.DataFrame = params["disaster"]
  context.preview(data)

  data.to_csv(os.path.join(params["dir"], params["name"] + ".csv"), index=False)
  
  return {"df": data}

