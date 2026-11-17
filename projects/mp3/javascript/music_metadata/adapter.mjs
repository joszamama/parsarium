// Local bytes reach music-metadata's documented parseBuffer/parseFile/parseStream; audio/mpeg selects lib/mpeg/MpegParser.js.
import { createReadStream } from 'node:fs';
import { parseBuffer, parseFile, parseStream } from 'music-metadata';

// duration: true makes MpegParser walk every frame to EOF instead of estimating from file size.
const options = { duration: true, skipCovers: true };

function summarize(metadata) {
  const { format, quality } = metadata;
  const codec = /^MPEG (1|2|2\.5) Layer ([123])$/.exec(format.codec ?? '');
  if (!codec) throw new Error(`no MPEG audio frames: ${format.codec}`);
  return {
    container: format.container,
    codec: format.codec,
    mpeg_version: Number(codec[1]),
    layer: Number(codec[2]),
    codec_profile: format.codecProfile,
    sample_rate: format.sampleRate,
    channels: format.numberOfChannels,
    bitrate: format.bitrate,
    number_of_samples: format.numberOfSamples,
    duration: format.duration,
    tag_types: format.tagTypes,
    warnings: quality.warnings.length,
  };
}

export async function parse(bytes) {
  return summarize(await parseBuffer(bytes, { mimeType: 'audio/mpeg', size: bytes.length }, options));
}

export async function parsePath(path) {
  return summarize(await parseFile(path, options));
}

export async function parseReadable(path) {
  return summarize(await parseStream(createReadStream(path), { mimeType: 'audio/mpeg' }, options));
}
