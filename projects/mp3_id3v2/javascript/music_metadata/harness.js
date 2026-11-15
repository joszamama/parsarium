async function parseMp3(data) {
  if (!data || data.length === 0 || data.length > (1 << 20)) {
    throw new Error('input outside harness limit');
  }
  const { parseBuffer } = await import('music-metadata');
  const meta = await parseBuffer(Buffer.from(data), { mimeType: 'audio/mpeg' },
    { maxMemoryAllocation: 1 << 20 });
  return { title: meta.common.title, artist: meta.common.artist,
           album: meta.common.album, sampleRate: meta.format.sampleRate };
}
module.exports = { parseMp3 };
