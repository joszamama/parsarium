"use strict";
const { parseData } = require("./harness");
module.exports.fuzz = async function fuzz(data) { await parseData(data); };
