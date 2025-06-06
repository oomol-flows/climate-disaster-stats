from json import JSONDecodeError
import typing
#region generated meta
from oocana import Context, LLMModelOptions
class Inputs(typing.TypedDict):
    input: LLMModelOptions
class Outputs(typing.TypedDict):
    output: typing.Any
#endregion

def main(params: Inputs, context: Context) -> Outputs:
    # your code

    return { "output": "output_value" }
