import { mkdtemp, readFile, readdir, realpath, rm } from 'node:fs/promises';
import { text as streamText } from 'node:stream/consumers';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { Readable } from 'node:stream';

export async function parse(name, path) {

if (!name || !path) {
  console.error('usage: node adapters/javascript/zip.mjs <package> <ZIP path>');
  process.exit(2);
}
const bytes = await readFile(path);
let result;
const fromFiles = (files) => ({ entries: files.map((file) => file.path), content: files[0].data.toString('utf8') });
async function extractToTemp(callback) {
  const directory = await mkdtemp(join(tmpdir(), 'parsarium-zip-'));
  try {
    await callback(directory);
    const entries = await readdir(directory);
    return { entries, content: await readFile(join(directory, entries[0]), 'utf8') };
  } finally { await rm(directory, { recursive: true, force: true }); }
}

switch (name) {
  case 'jszip': {
    const JSZip = (await import('jszip')).default;
    const zip = await JSZip.loadAsync(bytes);
    const names = Object.keys(zip.files).filter((entry) => !zip.files[entry].dir);
    result = { entries: names, content: await zip.file(names[0]).async('string') };
    break;
  }
  case 'adm-zip': {
    const AdmZip = (await import('adm-zip')).default;
    const zip = new AdmZip(bytes);
    const entries = zip.getEntries().filter((entry) => !entry.isDirectory);
    result = { entries: entries.map((entry) => entry.entryName), content: zip.readAsText(entries[0]) };
    break;
  }
  case 'yauzl': {
    const yauzl = (await import('yauzl')).default;
    const zip = await yauzl.fromBufferPromise(bytes);
    const entries = [];
    let content;
    for await (const entry of zip.eachEntry()) {
      if (entry.fileName.endsWith('/')) continue;
      entries.push(entry.fileName);
      const stream = await zip.openReadStreamPromise(entry);
      content = await streamText(stream);
    }
    result = { entries, content };
    break;
  }
  case 'unzipper': {
    const unzipper = (await import('unzipper')).default;
    const zip = await unzipper.Open.buffer(bytes);
    const entries = zip.files.filter((entry) => entry.type === 'File');
    result = { entries: entries.map((entry) => entry.path), content: (await entries[0].buffer()).toString('utf8') };
    break;
  }
  case 'fflate': {
    const { unzipSync } = await import('fflate');
    const files = unzipSync(bytes);
    const names = Object.keys(files);
    result = { entries: names, content: new TextDecoder().decode(files[names[0]]) };
    break;
  }
  case '@zip.js/zip.js': {
    const { ZipReader, Uint8ArrayReader, TextWriter } = await import('@zip.js/zip.js');
    const zip = new ZipReader(new Uint8ArrayReader(bytes));
    try {
      const entries = (await zip.getEntries()).filter((entry) => !entry.directory);
      result = { entries: entries.map((entry) => entry.filename), content: await entries[0].getData(new TextWriter()) };
    } finally { await zip.close(); }
    break;
  }
  case 'node-stream-zip': {
    const StreamZip = (await import('node-stream-zip')).default;
    const zip = new StreamZip.async({ file: path });
    try {
      const entries = Object.values(await zip.entries()).filter((entry) => !entry.isDirectory);
      result = { entries: entries.map((entry) => entry.name), content: (await zip.entryData(entries[0].name)).toString('utf8') };
    } finally { await zip.close(); }
    break;
  }
  case 'extract-zip': {
    const extract = (await import('extract-zip')).default;
    const directory = await mkdtemp(join(tmpdir(), 'parsarium-zip-'));
    try {
      const entries = [];
      await extract(join(process.cwd(), path), { dir: directory, onEntry: (entry) => entries.push(entry.fileName) });
      result = { entries, content: await readFile(join(directory, entries[0]), 'utf8') };
    } finally { await rm(directory, { recursive: true, force: true }); }
    break;
  }
  case '@electron-internal/extract-zip': {
    const extract = (await import('@electron-internal/extract-zip')).default;
    result = await extractToTemp((directory) => extract(join(process.cwd(), path), { dir: directory }));
    break;
  }
  case 'yauzl-promise': {
    const { fromBuffer } = await import('yauzl-promise');
    const zip = await fromBuffer(bytes);
    const entries = [];
    let content;
    try {
      for await (const entry of zip) {
        if (entry.filename.endsWith('/')) continue;
        entries.push(entry.filename);
        content = await streamText(await entry.openReadStream());
      }
    } finally { await zip.close(); }
    result = { entries, content };
    break;
  }
  case 'decompress-unzip': {
    const plugin = (await import('decompress-unzip')).default;
    result = fromFiles(await plugin()(bytes));
    break;
  }
  case '@xhmikosr/decompress-unzip': {
    const plugin = (await import('@xhmikosr/decompress-unzip')).default;
    result = fromFiles(await plugin()(bytes));
    break;
  }
  case 'decompress': {
    const decompress = (await import('decompress')).default;
    result = fromFiles(await decompress(bytes));
    break;
  }
  case '@xhmikosr/decompress': {
    const decompress = (await import('@xhmikosr/decompress')).default;
    result = fromFiles(await decompress(bytes));
    break;
  }
  case 'unzipper-esm': {
    const { Open } = await import('unzipper-esm');
    const zip = await Open.buffer(bytes);
    const entries = zip.files.filter((entry) => entry.type === 'File');
    result = { entries: entries.map((entry) => entry.path), content: (await entries[0].buffer()).toString('utf8') };
    break;
  }
  case 'pizzip': {
    const PizZip = (await import('pizzip')).default;
    const zip = new PizZip(bytes);
    const names = Object.keys(zip.files).filter((name) => !zip.files[name].dir);
    result = { entries: names, content: zip.file(names[0]).asText() };
    break;
  }
  case 'node-zip': {
    const NodeZip = (await import('node-zip')).default;
    const zip = new NodeZip(bytes, { base64: false });
    const names = Object.keys(zip.files).filter((name) => !zip.files[name].dir);
    result = { entries: names, content: zip.file(names[0]).asText() };
    break;
  }
  case 'unzip-stream': {
    const unzip = (await import('unzip-stream')).default;
    const entries = [];
    let content;
    for await (const entry of Readable.from([bytes]).pipe(unzip.Parse())) {
      if (entry.type !== 'File') { entry.autodrain(); continue; }
      entries.push(entry.path);
      content = await streamText(entry);
    }
    result = { entries, content };
    break;
  }
  case '@loaders.gl/zip': {
    const { ZipLoader } = await import('@loaders.gl/zip');
    const arrayBuffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
    const files = await ZipLoader.parse(arrayBuffer);
    const names = Object.keys(files);
    result = { entries: names, content: new TextDecoder().decode(files[names[0]]) };
    break;
  }
  case 'decompress-zip': {
    const DecompressZip = (await import('decompress-zip')).default;
    result = await extractToTemp((directory) => new Promise((resolve, reject) => {
      const zip = new DecompressZip(join(process.cwd(), path));
      zip.on('extract', resolve);
      zip.on('error', reject);
      zip.extract({ path: directory });
    }));
    break;
  }
  case 'zip-lib': {
    const { extract } = await import('zip-lib');
    result = await extractToTemp(async (directory) => extract(bytes, await realpath(directory)));
    break;
  }
  default:
    throw new Error(`unknown package: ${name}`);
}

return result;
}
