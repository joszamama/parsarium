async function parsePly(data) {
  if (!data || data.length === 0 || data.length > (1 << 20)) {
    throw new Error('input outside harness limit');
  }
  const bytes = Buffer.from(data);
  const arrayBuffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
  const { PLYLoader } = await import('three/addons/loaders/PLYLoader.js');
  const geometry = new PLYLoader().parse(arrayBuffer);
  const values = Array.from(geometry.getAttribute('position').array);
  const vertices = [];
  for (let i = 0; i < values.length; i += 3) vertices.push(values.slice(i, i + 3));
  const faces = [];
  // A geometry without an index (a point cloud) has no faces.
  const indices = geometry.index ? Array.from(geometry.index.array) : [];
  for (let i = 0; i < indices.length; i += 3) faces.push(indices.slice(i, i + 3));
  return { vertices, faces };
}
module.exports = { parsePly };
