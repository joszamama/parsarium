async function parseMp4(data) {
  if (!data || data.length === 0 || data.length > (1 << 20)) {
    throw new Error('input outside harness limit');
  }
  const { parseBuffer } = await import('music-metadata');
  const meta = await parseBuffer(Buffer.from(data), { mimeType: 'video/mp4' },
    { maxMemoryAllocation: 1 << 20 });
  const video = meta.format.trackInfo.find(track => track.type === 1);
  const audio = meta.format.trackInfo.find(track => track.type === 2);
  // Fields of a track the input does not have stay undefined and are left out of the JSON output.
  // width/height are the coded frame size from the visual sample entry (pixelWidth/pixelHeight);
  // displayWidth/displayHeight are the tkhd presentation size, which a file may set differently.
  return { title: meta.common.title,
           width: video?.video?.pixelWidth, height: video?.video?.pixelHeight,
           sampleRate: audio?.audio?.samplingFrequency };
}
module.exports = { parseMp4 };
