import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const mp3Parser = require('mp3-parser');

function rejected(message) {
  const error = new Error(message);
  error.name = 'ParseRejectedError';
  throw error;
}

export function parse(bytes) {
  const view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  let offset = 0;
  let frames = 0;
  let totalSamples = 0;
  let first = null;
  const variants = new Set();
  while (offset < view.byteLength) {
    const frame = mp3Parser.readFrame(view, offset, false);
    if (!frame || frame._section.offset !== offset ||
        !Number.isInteger(frame._section.byteLength) || frame._section.byteLength <= 0 ||
        offset + frame._section.byteLength > view.byteLength)
      rejected(`no complete MPEG audio frame at byte ${offset}`);
    const header = frame.header;
    if (header.layerDescription !== 'Layer III') rejected('not MPEG Layer III');
    if (!first) first = header;
    variants.add(`${header.mpegAudioVersionBits}|${header.samplingRate}|` +
                 `${header.channelModeBits}|${header.bitrate}|${frame._section.sampleLength}`);
    totalSamples += frame._section.sampleLength;
    offset += frame._section.byteLength;
    frames++;
  }
  if (!first) rejected('no MPEG audio frames');
  return {
    codec: 'mp3',
    mpeg_version_bits: first.mpegAudioVersionBits,
    layer: first.layerDescription,
    sample_rate: first.samplingRate,
    channels: first.channelModeBits === '11' ? 1 : 2,
    bitrate: first.bitrate * 1000,
    frames,
    frame_bytes: offset,
    samples_per_frame: totalSamples / frames,
    total_samples: totalSamples,
    header_variants: variants.size,
  };
}
