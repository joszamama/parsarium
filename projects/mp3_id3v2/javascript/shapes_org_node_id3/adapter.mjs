import { createReadStream } from 'node:fs';
import { readFile } from 'node:fs/promises';

export async function parse(name, control) {

if (!name || !control) throw new Error('usage: node adapters/javascript/mp3_id3v2.mjs PACKAGE CONTROL_PATH');
const bytes = await readFile(control);
const arrayBuffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
const clean = (value) => String(value ?? '').replace(/\0+$/, '');
const tags = (title, artist, album) => ({ title: clean(title), artist: clean(artist), album: clean(album) });
let result;

if (name === 'music-metadata') {
  const { parseFile } = await import(name);
  const meta = await parseFile(control);
  result = { ...tags(meta.common.title, meta.common.artist, meta.common.album), sampleRate: meta.format.sampleRate };
} else if (name === 'mediainfo.js') {
  const { default: factory } = await import(name);
  const analyzer = await factory();
  const parsed = await analyzer.analyzeData(bytes.length, (size, offset) => bytes.subarray(offset, offset + size));
  analyzer.close();
  const general = parsed.media.track.find((track) => track['@type'] === 'General');
  result = tags(general.Title, general.Performer, general.Album);
} else if (name === 'jsmediatags') {
  const { default: reader } = await import(name);
  const parsed = await new Promise((resolve, reject) => reader.read(bytes, { onSuccess: resolve, onError: reject }));
  result = { ...tags(parsed.tags.title, parsed.tags.artist, parsed.tags.album), version: parsed.version };
} else if (name === '@dantheman827/taglib-ts') {
  const { readTags } = await import('@dantheman827/taglib-ts/simpleApi.js');
  const parsed = await readTags(bytes);
  result = tags(parsed.title, parsed.artist, parsed.album);
} else if (name === '@audio/decode' || name === '@audio/decode-mp3') {
  const { default: decode } = await import(name);
  const audio = await decode(bytes);
  result = { sampleRate: audio.sampleRate, channels: audio.channelData.length, samples: audio.channelData[0].length };
} else if (name === 'get-audio-duration') {
  const { getAudioDurationInSeconds } = await import(name);
  result = { duration_ms: Math.round(1000 * await getAudioDurationInSeconds(control)) };
} else if (name === 'node-id3' || name === '@shapes-org/node-id3') {
  const api = await import(name);
  const parsed = api.default.read(bytes);
  result = tags(parsed.title, parsed.artist, parsed.album);
} else if (name === 'id3js') {
  const { fromPath } = await import(name);
  const parsed = await fromPath(control);
  result = { ...tags(parsed.title, parsed.artist, parsed.album), version: parsed.version };
} else if (name === 'mp3-duration') {
  const { default: duration } = await import(name);
  const seconds = await new Promise((resolve, reject) => duration(bytes, (error, value) => error ? reject(error) : resolve(value)));
  result = { duration_ms: Math.round(seconds * 1000) };
} else if (name === 'get-mp3-duration') {
  const { default: duration } = await import(name);
  result = { duration_ms: duration(bytes) };
} else if (name === 'mp3tag.js') {
  const { default: MP3Tag } = await import(name);
  const reader = new MP3Tag(bytes);
  reader.read();
  if (reader.error) throw new Error(reader.error);
  result = tags(reader.tags.v2.TIT2, reader.tags.v2.TPE1, reader.tags.v2.TALB);
} else if (name === 'jamp3') {
  const { ID3v2 } = await import(name);
  const parsed = ID3v2.simplify(await new ID3v2().read(control));
  result = tags(parsed.TITLE, parsed.ARTIST, parsed.ALBUM);
} else if (name === 'audio-tag') {
  const { read } = await import(name);
  const parsed = read(bytes);
  result = { ...tags(parsed.metadata.title, parsed.metadata.artist?.[0], parsed.metadata.album), format: parsed.format };
} else if (name === 'audiotagr') {
  const { readAudioMetadata } = await import(name);
  const parsed = await readAudioMetadata(control);
  result = tags(parsed.title, parsed.artist, parsed.album);
} else if (name === 'id3v2') {
  const { ID3v2 } = await import(name);
  const parsed = new ID3v2(control);
  result = tags(parsed.title, parsed.artist, parsed.album);
} else if (name === 'id3-parser') {
  const api = await import(name);
  const parsed = api.default.default(bytes);
  result = tags(parsed.title, parsed.artist, parsed.album);
} else if (name === 'mp3-parser') {
  const { default: api } = await import(name);
  const parsed = api.readId3v2Tag(new DataView(arrayBuffer));
  const field = (id) => parsed.frames.find((frame) => frame.header.id === id)?.content?.value;
  result = { ...tags(field('TIT2'), field('TPE1'), field('TALB')), version: parsed.header.majorVersion };
} else if (name === 'id3-meta') {
  const api = await import(name);
  const parsed = api.default.default(arrayBuffer);
  result = tags(parsed.TIT2?.text, parsed.TPE1?.text, parsed.TALB?.text);
} else if (name === 'mp3tag') {
  const { readHeader } = await import(name);
  const parsed = await readHeader(control);
  const field = (id) => parsed.decoder.decodeString(parsed.getFrameBuffer(id));
  result = tags(field('TIT2'), field('TPE1'), field('TALB'));
} else if (name === 'id3-reader') {
  const { default: read } = await import(name);
  const parsed = await read(control);
  result = tags(parsed.title, parsed.singer, parsed.album);
} else if (name === 'simple-id3.js') {
  const { default: ID3 } = await import(name);
  const parsed = new ID3(bytes).asObject();
  result = tags(parsed.TIT2, parsed.TPE1, parsed.TALB);
} else if (name === 'id3v2-parser') {
  const { default: ID3Parser } = await import(name);
  const parsed = [];
  await new Promise((resolve, reject) => {
    const stream = createReadStream(control).pipe(new ID3Parser());
    stream.on('data', (value) => parsed.push(value));
    stream.on('end', resolve);
    stream.on('error', reject);
  });
  const field = (id) => parsed.find((item) => item.type === id)?.value;
  result = tags(field('TIT2'), field('TPE1'), field('TALB'));
} else throw new Error(`unsupported package: ${name}`);

if (Object.values(result).some((value) => value === undefined || value === null || value === '')) throw new Error(`${name} returned missing parsed fields`);
return result;
}
