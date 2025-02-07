from oocana import Context
import pandas as pd
import os.path


def main(params: dict, context: Context):
    f = params["csv"]
    # check file is exist
    backup_path = os.path.join(
        os.path.dirname(params["csv"]), "backup_" + os.path.basename(params["csv"])
    )
    with open(params["csv"], "rb") as src_file, open(backup_path, "wb") as dest_file:
        dest_file.write(src_file.read())
    if os.path.exists(f) == False:
        raise Exception(f"File {f} is not exist")

    data = pd.read_csv(f)
    context.preview(data)
    return {"dataframe": data}
