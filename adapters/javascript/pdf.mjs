import { readFile } from 'node:fs/promises';

const [name, path] = process.argv.slice(2);
if (!name || !path) throw new Error('usage: node adapters/javascript/pdf.mjs <package> <PDF path>');
const bytes = await readFile(path);
const text = (value) => ({ text: String(value).trim() });
let output;

switch (name) {
  case 'pdfjs-dist': {
    const { getDocument } = await import('pdfjs-dist/legacy/build/pdf.mjs');
    const task = getDocument({ data: new Uint8Array(bytes), useSystemFonts: true });
    try {
      const pdf = await task.promise;
      const page = await pdf.getPage(1);
      output = text((await page.getTextContent()).items.map((item) => item.str).join(' '));
    } finally { await task.destroy(); }
    break;
  }
  case 'pdf-lib': {
    const { PDFDocument } = await import(name);
    const pdf = await PDFDocument.load(bytes);
    output = { pages: pdf.getPageCount(), title: pdf.getTitle() };
    break;
  }
  case 'pdf-parse': {
    const { PDFParse } = await import(name);
    const parser = new PDFParse({ data: bytes });
    try { output = text((await parser.getText()).pages.map((page) => page.text).join(' ')); }
    finally { await parser.destroy(); }
    break;
  }
  case 'unpdf': {
    const { extractText } = await import(name);
    output = text((await extractText(new Uint8Array(bytes), { mergePages: true })).text);
    break;
  }
  case 'clawpdf': {
    const { openPdf } = await import(name);
    await using pdf = await openPdf(path);
    output = text(pdf.page(1).text());
    break;
  }
  case 'officeparser': {
    const { OfficeParser } = await import(name);
    const ast = await OfficeParser.parseOffice(bytes);
    output = text((await ast.to('text')).value);
    break;
  }
  case 'mupdf': {
    const mupdf = (await import(name)).default;
    const pdf = mupdf.Document.openDocument(path);
    output = text(pdf.loadPage(0).toStructuredText().asText());
    break;
  }
  case 'pdf2json': {
    const PDFParser = (await import(name)).default;
    const parser = new PDFParser();
    const data = await new Promise((resolve, reject) => {
      parser.on('pdfParser_dataReady', resolve);
      parser.on('pdfParser_dataError', (error) => reject(error.parserError));
      parser.parseBuffer(bytes);
    });
    output = text(data.Pages.flatMap((page) => page.Texts.flatMap((item) => item.R.map((run) => decodeURIComponent(run.T)))).join(' '));
    break;
  }
  case 'pdf.js-extract': {
    const { PDFExtract } = await import(name);
    const data = await new PDFExtract().extractBuffer(bytes, {});
    output = text(data.pages.flatMap((page) => page.content.map((item) => item.str)).join(' '));
    break;
  }
  case 'pdfreader': {
    const { PdfReader } = await import(name);
    const items = await new Promise((resolve, reject) => {
      const found = [];
      new PdfReader().parseBuffer(bytes, (error, item) => {
        if (error) reject(error);
        else if (!item) resolve(found);
        else if (item.text) found.push(item.text);
      });
    });
    output = text(items.join(' '));
    break;
  }
  case 'office-text-extractor': {
    const { getTextExtractor } = await import(name);
    const extracted = await getTextExtractor().extractText({ input: bytes, type: 'buffer' });
    output = text(extracted.replace(/\n\s*--\s+\d+ of \d+\s+--\s*$/, ''));
    break;
  }
  case 'pdf-parse-new': {
    const parse = (await import(name)).default;
    output = text((await parse(bytes)).text);
    break;
  }
  case 'pdf-text-reader': {
    const { readPdfText } = await import(name);
    output = text(await readPdfText({ url: path }));
    break;
  }
  case 'pdf-ts': {
    const { pdfToText } = await import(name);
    output = text(await pdfToText(bytes));
    break;
  }
  case 'pdfdataextract': {
    const { PdfData } = await import(name);
    output = text((await PdfData.extract(bytes)).text.join(' '));
    break;
  }
  case 'pdfnano': {
    const { PDFParser } = await import(name);
    output = text((await new PDFParser().parseFile(path)).text);
    break;
  }
  case 'pdf-parser.js': {
    const { readPdf } = await import(name);
    const document = readPdf(bytes);
    output = text(document.pages.flatMap((page) => page.items.filter((item) => item.kind === 'text').map((item) => item.text)).join(' '));
    break;
  }
  case 'coherentpdf': {
    const cpdf = (await import(name)).default;
    const pdf = cpdf.fromFile(path, '');
    try { output = { pages: cpdf.pages(pdf) }; }
    finally { cpdf.deletePdf(pdf); }
    break;
  }
  case 'pdfnative': {
    const { extractText } = await import(name);
    output = text(extractText(bytes).map((page) => page.text).join(' '));
    break;
  }
  case 'afpp': {
    const { pdf2string } = await import(name);
    output = text((await pdf2string(path)).join(' '));
    break;
  }
  case 'rasgapdf': {
    const { extractText } = await import(name);
    output = text(extractText(bytes));
    break;
  }
  case '@firecrawl/pdf-inspector-wasm': {
    const { default: init, extractText } = await import(name);
    const wasm = await readFile(new URL('./pdf_inspector_wasm_bg.wasm', import.meta.resolve(name)));
    await init({ module_or_path: wasm });
    output = text(extractText(bytes));
    break;
  }
  default:
    throw new Error(`unknown package: ${name}`);
}

console.log(JSON.stringify(output));
