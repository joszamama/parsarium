import { readFile } from 'node:fs/promises';
import { Readable } from 'node:stream';

export async function parse(name, path) {

if (!name || !path) throw new Error('usage: node adapters/javascript/wav.mjs <package> <WAV path>');
const bytes = await readFile(path);
// A decoder that returns no channels (audio-decode's empty result) decoded no
// audio from the file; that is reported as a rejection, not as zero samples.
const decoded = (audio) => {
  if (!audio.channelData.length) throw new Error(`${name} decoded no audio: empty result (no channels, sample rate ${audio.sampleRate})`);
  return {
    sampleRate: audio.sampleRate,
    channels: audio.channelData.length,
    sampleCount: audio.channelData[0].length,
    sampleSigns: Array.from(audio.channelData[0], (value) => Math.sign(value))
  };
};
const header = (sampleRate, channels, bitsPerSample) => ({ sampleRate, channels, bitsPerSample });
const fromWaveFile = (wave) => header(wave.fmt.sampleRate, wave.fmt.numChannels, wave.fmt.bitsPerSample);
const callback = (fn) => new Promise((resolve, reject) => fn((error, value) => error ? reject(error) : resolve(value)));
let output;

switch (name) {
  case 'music-metadata': {
    const { parseBuffer } = await import(name);
    const { format } = await parseBuffer(bytes, { mimeType: 'audio/wav' });
    output = header(format.sampleRate, format.numberOfChannels, format.bitsPerSample);
    break;
  }
  case 'mediainfo.js': {
    const factory = (await import(name)).default;
    const parser = await factory();
    try {
      const result = await parser.analyzeData(bytes.length, (size, offset) => bytes.subarray(offset, offset + size));
      const track = result.media.track.find((item) => item['@type'] === 'Audio');
      output = header(track.SamplingRate, track.Channels, track.BitDepth);
    } finally { parser.close(); }
    break;
  }
  case '@uttori/audio-wave': {
    const AudioWAV = (await import(name)).default;
    const parsed = AudioWAV.fromFile(bytes);
    const format = parsed.chunks.find((chunk) => chunk.type === 'format').value;
    output = header(format.sampleRate, format.channels, format.bitsPerSample);
    break;
  }
  case 'audio-decode':
  case '@audio/decode':
  case '@audio/decode-wav': {
    const decode = (await import(name)).default;
    output = decoded(await decode(bytes));
    break;
  }
  case 'node-wav':
  case 'wav-decoder': {
    const { decode } = await import(name);
    output = decoded(await decode(bytes));
    break;
  }
  case 'wav-decoder-ts': {
    const decoder = (await import(name)).default.default;
    output = decoded(await decoder.decode(bytes));
    break;
  }
  case 'wav-reader-ts': {
    const decoder = (await import(name)).default.default;
    output = decoded((await decoder.decode(bytes)).data);
    break;
  }
  case 'wav-file-decoder': {
    const { decodeWavFile } = await import(name);
    output = decoded(decodeWavFile(bytes));
    break;
  }
  case 'wavefile':
  case 'prx-wavefile':
  case '@ra2web/wavefile': {
    const module = await import(name);
    const WaveFile = module.WaveFile ?? module.default.WaveFile;
    output = fromWaveFile(new WaveFile(bytes));
    break;
  }
  case 'wavefile-reader': {
    const { WaveFileReader } = (await import(name)).default;
    output = fromWaveFile(new WaveFileReader(bytes));
    break;
  }
  case 'wavefile-parser': {
    const { WaveFileParser } = (await import(name)).default;
    output = fromWaveFile(new WaveFileParser(bytes));
    break;
  }
  case 'wav-file-info':
  case 'wav-info': {
    const reader = (await import(name)).default;
    const info = name === 'wav-file-info'
      ? await callback((done) => reader.infoByFilename(path, done))
      : await callback((done) => reader.infoByBuffer(bytes, done));
    output = header(info.header.sample_rate, info.header.num_channels, info.header.bits_per_sample);
    break;
  }
  case 'node-bwf-wav-file-reader': {
    const { readSync } = await import(name);
    const { result } = await readSync(path);
    output = header(result.sampleRate, result.numChannels, result.bitsPerSample);
    break;
  }
  case 'wav-audio-length': {
    const duration = (await import(name)).default.default;
    output = { durationSeconds: duration(bytes) };
    break;
  }
  case 'get-audio-duration': {
    const { getAudioDurationInSeconds } = await import(name);
    output = { durationSeconds: await getAudioDurationInSeconds(path) };
    break;
  }
  case 'wav': {
    const { Reader } = await import(name);
    const reader = new Reader();
    const chunks = [];
    const format = await new Promise((resolve, reject) => {
      reader.on('format', resolve);
      reader.on('data', (chunk) => chunks.push(chunk));
      reader.on('error', reject);
      Readable.from([bytes]).pipe(reader);
    });
    output = header(format.sampleRate, format.channels, format.bitDepth);
    break;
  }
  default:
    throw new Error(`unknown package: ${name}`);
}

return output;
}
