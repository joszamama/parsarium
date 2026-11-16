import { createReadStream } from 'node:fs';
import { readFile as readFileAsync } from 'node:fs/promises';

export async function parse(name, control) {

if (!name || !control) throw new Error('usage: node adapters/javascript/mp4.mjs PACKAGE CONTROL_PATH');
const bytes = await readFileAsync(control);
let result;

if (name === 'music-metadata') {
  const { parseFile } = await import(name);
  const meta = await parseFile(control);
  const video = meta.format.trackInfo.find((track) => track.type === 1);
  const audio = meta.format.trackInfo.find((track) => track.type === 2);
  result = { title: meta.common.title, width: video.video.displayWidth, height: video.video.displayHeight, sampleRate: audio.audio.samplingFrequency };
} else if (name === 'mediainfo.js') {
  const { default: mediaInfoFactory } = await import(name);
  const analyzer = await mediaInfoFactory();
  const parsed = await analyzer.analyzeData(bytes.length, (size, offset) => bytes.subarray(offset, offset + size));
  analyzer.close();
  const general = parsed.media.track.find((track) => track['@type'] === 'General');
  const video = parsed.media.track.find((track) => track['@type'] === 'Video');
  const audio = parsed.media.track.find((track) => track['@type'] === 'Audio');
  result = { title: general.Title, width: Number(video.Width), height: Number(video.Height), sampleRate: Number(audio.SamplingRate) };
} else if (name === 'codem-isoboxer') {
  const { default: ISOBoxer } = await import(name);
  const file = ISOBoxer.parseBuffer(bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength));
  result = { boxes: file.boxes.map((box) => box.type), brand: file.fetch('ftyp').major_brand };
} else if (name === 'mp4box') {
  const { createFile } = await import(name);
  const file = createFile();
  let info;
  file.onReady = (value) => { info = value; };
  const buffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
  buffer.fileStart = 0;
  file.appendBuffer(buffer);
  file.flush();
  result = { brand: info.brands[0], width: info.videoTracks[0].video.width, height: info.videoTracks[0].video.height, tracks: info.tracks.length };
} else if (name === 'isobmff-inspector') {
  const { default: inspect } = await import(name);
  const tree = await inspect(bytes);
  result = { boxes: tree.map((box) => box.type), brand: tree[0].values.find((value) => value.key === 'major_brand').value };
} else if (name === 'mediabunny') {
  const { Input, BufferSource, ALL_FORMATS } = await import(name);
  const input = new Input({ source: new BufferSource(bytes), formats: ALL_FORMATS });
  const tracks = await input.getTracks();
  const video = tracks.find((track) => track.type === 'video');
  const audio = tracks.find((track) => track.type === 'audio');
  result = { format: (await input.getFormat()).name, duration: await input.computeDuration(), width: video.displayWidth, height: video.displayHeight, audioCodec: audio.codec };
} else if (name === '@audio/decode-mp4') {
  const { default: decode } = await import(name);
  const audio = await decode(bytes);
  result = { sampleRate: audio.sampleRate, channels: audio.channelData.length, samples: audio.channelData[0].length };
} else if (name === 'jsmediatags') {
  const { default: tags } = await import(name);
  const parsed = await new Promise((resolve, reject) => tags.read(bytes, { onSuccess: resolve, onError: reject }));
  result = { type: parsed.type, brand: parsed.ftyp, title: parsed.tags.title };
} else if (name === 'mp4-box-encoding') {
  const { default: encoding } = await import(name);
  const parsed = encoding.decode(bytes.subarray(0, bytes.readUInt32BE(0)));
  result = { type: parsed.type, brand: parsed.brand, compatible: parsed.compatibleBrands };
} else if (name === 'node-video-lib') {
  const { MovieParser } = await import(name);
  const fs = await import('node:fs');
  const fd = fs.openSync(control, 'r');
  try {
    const movie = MovieParser.parse(fd);
    result = { duration: movie.relativeDuration(), tracks: movie.tracks.length };
  } finally { fs.closeSync(fd); }
} else if (name === 'mp4reader') {
  const { Mp4DecodeByModule } = await import(name);
  const parsed = await Mp4DecodeByModule(control, ['ftyp', 'hdlr']);
  result = { brand: parsed.ftyp.Major_brand, handlers: parsed.hdlr.map((value) => value.Handler_type) };
} else if (name === 'mediafile-metadata') {
  const { getEssentials } = await import(name);
  const parsed = await getEssentials(control);
  result = { creationDate: parsed.creationDate };
} else if (name === 'mp4-parser') {
  const { default: MP4Parser } = await import(name);
  const tags = [];
  await new Promise((resolve, reject) => {
    const parser = createReadStream(control).pipe(new MP4Parser());
    parser.on('data', (tag) => tags.push(tag));
    parser.on('end', resolve);
    parser.on('error', reject);
  });
  result = { title: tags.find((tag) => tag.type === '�nam')?.value, duration: tags.find((tag) => tag.type === 'duration')?.value };
} else if (name === 'mp4-stream') {
  const { decode } = await import(name);
  const stream = decode();
  const types = [];
  await new Promise((resolve, reject) => {
    stream.on('box', (box) => { types.push(box.type); stream.ignore(); });
    stream.on('finish', resolve);
    stream.on('error', reject);
    stream.end(bytes);
  });
  result = { boxes: types };
} else if (name === 'fmp4.js') {
  const { default: parser } = await import(name);
  const stream = parser.parse();
  await new Promise((resolve, reject) => { stream.on('finish', resolve); stream.on('error', reject); stream.end(bytes); });
  result = { boxes: parser.boxes.map((box) => box.hdr.type) };
} else if (name === '@isomp4/parser') {
  const { MP4Parser } = await import(name);
  const parser = new MP4Parser();
  const types = [];
  parser.boxStarted = (header) => { types.push(header.type); return false; };
  parser.append(bytes);
  result = { boxes: types };
} else if (name === 'mp4tree') {
  const { MP4Tree } = await import(name);
  const tree = await new MP4Tree(control).parse();
  result = { valid: tree.isValid, boxes: tree.root.children.map((box) => box.name) };
} else if (name === 'metaprobe') {
  const { extractMeta } = await import(name);
  const meta = await extractMeta(control, { hash: false });
  result = { kind: meta.kind, format: meta.format, width: meta.width, height: meta.height, title: meta.metadata['�nam'], duration: meta.duration };
} else if (name === '@dantheman827/taglib-ts') {
  const { readTags } = await import('@dantheman827/taglib-ts/simpleApi.js');
  const tags = await readTags(bytes);
  result = { title: tags.title, sampleRate: tags.audioProperties.sampleRate, channels: tags.audioProperties.channels };
} else if (name === 'mp4-metadata') {
  // The package expects the browser FileReader API. This tiny adapter implements
  // its readAsArrayBuffer contract with the standard Blob.arrayBuffer method.
  globalThis.FileReader = class {
    async readAsArrayBuffer(blob) {
      try { this.result = await blob.arrayBuffer(); this.onload?.(); }
      catch (error) { this.onerror?.(error); }
    }
  };
  const { default: metadataModule } = await import(name);
  const metadata = metadataModule.default;
  result = { creationTime: await metadata.getCreationTime(new Blob([bytes]), { maxBytesRead: bytes.length }) };
} else throw new Error(`unsupported package: ${name}`);

if (Object.values(result).some((value) => value === undefined || value === null)) throw new Error(`${name} returned missing parsed fields`);
return result;
}
