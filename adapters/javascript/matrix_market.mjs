import { readFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { parseMatrixMarket, get } from '@jtgtools/xsparse';
import { fromMatrixMarket } from '@statelyai/graph/matrix-market';

const require = createRequire(import.meta.url);
const ngraph = require('ngraph.serialization/mtx');
const [name, path] = process.argv.slice(2);
if (!name || !path) throw new Error('usage: node adapters/javascript/matrix_market.mjs PACKAGE CONTROL');
const text = await readFile(path, 'utf8');
let result;
switch (name) {
  case 'ngraph.serialization': {
    const graph = ngraph.load(text);
    result = { nodes: graph.getNodesCount(), edges: graph.getLinksCount(), edge_1_2: graph.hasLink(1, 2)?.data ?? null };
    break;
  }
  case '@statelyai/graph': {
    const graph = fromMatrixMarket(text);
    result = { nodes: graph.nodes.length, edges: graph.edges.length, edge_weight_0_1: graph.edges.find((e) => e.sourceId === '0' && e.targetId === '1')?.weight ?? null };
    break;
  }
  case '@jtgtools/xsparse': {
    const matrix = parseMatrixMarket(text);
    result = { rows: matrix.rows, cols: matrix.cols, value_0_2: get(matrix, 0, 2) };
    break;
  }
  default:
    throw new Error(`unknown Matrix Market package: ${name}`);
}
console.log(JSON.stringify(result));
