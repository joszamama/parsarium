import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { text as streamText } from 'node:stream/consumers';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [name, path] = process.argv.slice(2);
if (!name || !path) {
  console.error('usage: node adapters/javascript/zip.mjs <package> <ZIP path>');
  process.exit(2);
}
const bytes = await readFile(path);
let result;

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
  default:
    throw new Error(`unknown package: ${name}`);
}

console.log(JSON.stringify(result));
