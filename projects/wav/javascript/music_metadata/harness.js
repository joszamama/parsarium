async function parseWav(data) {
  if (!data || data.length === 0 || data.length > (1 << 20)) {
    throw new Error('input outside harness limit');
  }
  const { parseBuffer } = await import('music-metadata');
  const { format } = await parseBuffer(Buffer.from(data), { mimeType: 'audio/wav' },
    { maxMemoryAllocation: 1 << 20 });
  return {
    sampleRate: format.sampleRate,
    channels: format.numberOfChannels,
    bitsPerSample: format.bitsPerSample,
  };
}

module.exports = { parseWav };
