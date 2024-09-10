import type { Context } from "@oomol/types/oocana";

// "in", "out" is the default node key.
// Redefine the name and type of the node, change it manually below.
// Click on the gear(⚙) to configure the input output UI
type Inputs = Readonly<{ in: unknown }>;
type Outputs = Readonly<{ out: unknown }>;

export default async function(inputs: Inputs, context: Context<Inputs, Outputs>): Promise<Outputs> {
  // // This API can help preview several types of files
  // context.preview({
  //   // type -> "image","video", "audio", "markdown", "table", "iframe"
  //   type: "image",
  //   data: payload,
  // })
  return { out: null };
};
