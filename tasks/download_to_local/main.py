from oocana import Context

# "in", "out" is the default node key.
# Redefine the name and type of the node, change it manually below.
# Click on the gear(⚙) to configure the input output UI
import urllib.request

def main(inputs: dict, context: Context):
  url = inputs.get("online_url")
  file_name = inputs.get("file_name")
  folder = inputs.get("folder")
  file_local = folder+'/'+file_name
  # inputs.get("in") -> help you get node input value
  try:
    response = urllib.request.urlopen(url)
    with open(file_local, 'wb') as file:
        file.write(response.read())
    print("File downloaded successfully")
  except Exception as e:
    print(f"An error occurred: {e}")
  # preview pandas dataframe
  # context.preview(df)

  # context.preview({
  #   # type can be "image", "video", "audio", "markdown", "table", "iframe"
  #   "type": "image",
  #   # data can be file path, base64, pandas dataframe
  #   "data": "",
  # })

  return { "file_address": file_local }