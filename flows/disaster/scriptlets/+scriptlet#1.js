//#region generated meta
/**
 * @import { Context, LLMModelOptions } from "@oomol/types/oocana";
 * @typedef {{
 *   input: LLMModelOptions;
 * }} Inputs;
 * @typedef {{
 *   output: any;
 * }} Outputs;
 */
//#endregion

import { subscribe } from "diagnostics_channel";

/**
 * @param {Inputs} params
 * @param {Context<Inputs, Outputs>} context
 * @returns {Promise<Outputs>}
 */
export default async function (params, context) {

    // your code
    return { output: "output_value" };
}
