import { readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
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
  case '@orbifold/graphs': {
    const { MatrixMarket } = await import('@orbifold/graphs');
    const graph = MatrixMarket.parse(text);
    result = { nodes: graph.nodes.length, edges: graph.edges.length,
      edge_1_2: graph.edges.some((edge) => edge.sourceId === '1' && edge.targetId === '2') };
    break;
  }
  case 'scran.js': {
    const scran = await import('scran.js');
    await scran.initialize({ numberOfThreads: 1 });
    const data = await readFile(path);
    const dimensions = scran.extractMatrixMarketDimensions(data);
    const matrix = scran.initializeSparseMatrixFromMatrixMarket(data);
    result = { rows: matrix.numberOfRows(), cols: matrix.numberOfColumns(),
      lines: dimensions.lines, value_2_2: matrix.column(2)[2] };
    matrix.free();
    scran.terminate();
    break;
  }
  case 'bakana': {
    const bakana = await import('bakana');
    await bakana.initialize({ numberOfThreads: 1 });
    const directory = dirname(path);
    const dataset = new bakana.TenxMatrixMarketDataset(
      path, join(directory, 'features.tsv.gz'), join(directory, 'barcodes.tsv.gz'));
    const loaded = await dataset.load();
    const matrix = loaded.matrix.get('RNA');
    result = { rows: matrix.numberOfRows(), cols: matrix.numberOfColumns(),
      value_0_2: matrix.column(2)[0] };
    loaded.matrix.free();
    await bakana.terminate();
    break;
  }
  default:
    throw new Error(`unknown Matrix Market package: ${name}`);
}
console.log(JSON.stringify(result));
