import { createReadStream } from 'node:fs';
import { readFile } from 'node:fs/promises';
import { createRequire } from 'node:module';

export async function parse(name, path) {

if (!name || !path) throw new Error('usage: node ascii_ply.mjs PACKAGE CONTROL');
const bytes = await readFile(path);
const arrayBuffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
const verticesFromFlat = (flat) => {
  const numbers = Array.from(flat);
  return Array.from({ length: numbers.length / 3 }, (_, i) => numbers.slice(i * 3, i * 3 + 3));
};
const fromGeometry = (geometry) => ({
  vertices: verticesFromFlat(geometry.getAttribute('position').array),
  faces: [Array.from(geometry.index.array)]
});

let output;
if (name === 'three') {
  const { PLYLoader } = await import('three/addons/loaders/PLYLoader.js');
  output = fromGeometry(new PLYLoader().parse(arrayBuffer));
} else if (name === 'three-stdlib') {
  const { PLYLoader } = await import('three-stdlib');
  output = fromGeometry(new PLYLoader().parse(arrayBuffer));
} else if (name === '@loaders.gl/ply' || name === '@kibeo/loaders.gl-ply') {
  const { parse } = await import('@loaders.gl/core');
  const { PLYLoader } = await import(name);
  const mesh = await parse(arrayBuffer, PLYLoader);
  output = { vertices: verticesFromFlat(mesh.attributes.POSITION.value),
    faces: [Array.from(mesh.indices.value)] };
} else if (name === 'parse-ply') {
  const { default: parse } = await import('parse-ply');
  const mesh = await new Promise((resolve, reject) =>
    parse(createReadStream(path), (error, value) => error ? reject(error) : resolve(value)));
  output = { vertices: Array.from(mesh.vertex.x, (x, i) => [x, mesh.vertex.y[i], mesh.vertex.z[i]]),
    faces: mesh.face.vertex_indices.map((indices) => Array.from(indices)) };
} else if (name === 'plyparser') {
  const { default: parse } = await import('plyparser');
  const mesh = parse(bytes);
  output = { vertices: mesh.vertices, faces: mesh.faces };
} else if (name === 'ply-js') {
  const { readPlyFromLines } = await import('ply-js');
  const mesh = readPlyFromLines(bytes.toString('utf8').trimEnd().split(/\r?\n/));
  const vertex = mesh.elements.find((element) => element.name === 'vertex');
  const face = mesh.elements.find((element) => element.name === 'face');
  output = { vertices: vertex.data.map(({ x, y, z }) => [x, y, z]),
    faces: face.data.map(({ vertex_indices }) => vertex_indices) };
} else if (name === '@draco-rust/ply') {
  const { default: init, read_ply } = await import('@draco-rust/ply');
  await init({ module_or_path: await readFile(new URL('../../node_modules/@draco-rust/ply/index_bg.wasm', import.meta.url)) });
  const result = read_ply(bytes);
  if (!result.success) throw new Error(result.error);
  const mesh = result.meshes[0];
  output = { vertices: verticesFromFlat(mesh.positions), faces: [Array.from(mesh.indices)] };
} else if (name === 'three-ply-loader') {
  const base = await import('three');
  const THREE = { ...base, BufferGeometry: class extends base.BufferGeometry {
    addAttribute(key, value) { return this.setAttribute(key, value); }
  } };
  const { default: register } = await import('three-ply-loader');
  register(THREE);
  output = fromGeometry(new THREE.PLYLoader().parse(arrayBuffer));
} else if (name === 'three-ply-loader-ts') {
  const { default: module } = await import('three-ply-loader-ts');
  const originalLog = console.log;
  let geometry;
  try { console.log = () => {}; geometry = new module.default().parse(arrayBuffer); }
  finally { console.log = originalLog; }
  output = fromGeometry(geometry);
} else if (name === '@isopodlabs/binary_meshes') {
  const { formatOf } = await import('@isopodlabs/binary_meshes');
  const mesh = await formatOf('.ply').load(bytes);
  output = { vertices: mesh.points.map(({ x, y, z }) => [x, y, z]), faces: mesh.faces };
} else if (name === '@meshioplusplus/wasm') {
  const { loadMeshioPlusPlus } = await import('@meshioplusplus/wasm');
  const meshio = await loadMeshioPlusPlus({ variant: 'seq' });
  meshio.FS.writeFile('/triangle.ply', bytes);
  const mesh = meshio.readMesh('/triangle.ply');
  output = { vertices: verticesFromFlat(mesh.points),
    faces: mesh.cells.flatMap((cell) => cell.type === 'triangle' ? [Array.from(cell.data)] : []) };
} else if (name === 'online-3d-viewer') {
  const { ImporterPly } = await import('online-3d-viewer');
  const importer = new ImporterPly();
  importer.Import('triangle.ply', 'ply', arrayBuffer, {
    getDefaultLineMaterialColor: () => ({ r: 0, g: 0, b: 0 }),
    getDefaultMaterialColor: () => ({ r: 200, g: 200, b: 200 }),
    onError: () => {}, onSuccess: () => {}, onComplete: () => {}
  });
  if (importer.WasError()) throw new Error(importer.GetError?.() || 'PLY import failed');
  const mesh = importer.GetModel().GetMesh(0);
  output = { vertices: Array.from({ length: mesh.VertexCount() }, (_, i) => {
    const { x, y, z } = mesh.GetVertex(i); return [x, y, z];
  }), faces: Array.from({ length: mesh.TriangleCount() }, (_, i) => {
    const { v0, v1, v2 } = mesh.GetTriangle(i); return [v0, v1, v2];
  }) };
} else if (name === 'meshlab-ts') {
  const { CMeshO, readPly } = await import('meshlab-ts');
  const mesh = new CMeshO();
  readPly(mesh, bytes, 'triangle.ply');
  output = { vertices: verticesFromFlat(mesh.vertCoord.slice(0, mesh.vn * 3)),
    faces: verticesFromFlat(mesh.faceVert.slice(0, mesh.fn * 3)) };
} else if (name === 'modeltree') {
  const { loadModelFile } = await import('modeltree');
  const result = await loadModelFile(path);
  if (result.format.id !== 'ply') throw new Error('modeltree did not detect PLY');
  output = fromGeometry(result.root.geometry);
} else if (name === 'sunzi-plyloader') {
  const { PLYLoader } = await import('sunzi-plyloader');
  output = fromGeometry(new PLYLoader().parse(arrayBuffer));
} else if (name === 'point-cloud-convert') {
  const require = createRequire(import.meta.url);
  const convert = require('point-cloud-convert/point-cloud-convert.js');
  const ascii = convert(bytes.toString('ascii'), 'ply2asc');
  output = { vertices: ascii.trim().split(/\r?\n/).map((line) => line.split(/\s+/).map(Number)), faces: [] };
} else if (name === '@voxelkloud/format-single') {
  const { loadSingleFileSource } = await import('@voxelkloud/format-single');
  const source = await loadSingleFileSource('triangle.ply', { bytes, worker: false });
  output = { pointCount: source.pointCount, nodeCount: source.nodes.length,
    recordBytes: source.records.reduce((sum, records) => sum + records.byteLength, 0) };
} else if (name === '@voxelkloud/wasm-build') {
  const { initBuilder, buildFromFile } = await import('@voxelkloud/wasm-build');
  await initBuilder();
  const cloud = buildFromFile(bytes);
  output = { pointCount: cloud.pointCount, nodeCount: cloud.nodeCount,
    recordBytes: cloud.nodeRecords(0).byteLength };
} else if (name === 'threejs-ply-loader') {
  const require = createRequire(import.meta.url);
  const THREE = require('three-legacy-125');
  const makeLoader = require('threejs-ply-loader');
  const PLYLoader = makeLoader(THREE);
  output = fromGeometry(new PLYLoader().parse(arrayBuffer));
} else {
  throw new Error(`unknown ASCII PLY parser: ${name}`);
}

return output;
}
