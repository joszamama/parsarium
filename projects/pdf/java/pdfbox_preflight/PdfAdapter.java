package org.parsarium;

import java.nio.file.Path;

public final class PdfAdapter {
    private PdfAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("usage: PdfAdapter API CONTROL.pdf");
        Path path = Path.of(args[1]);
        int pages = switch (args[0]) {
            case "pdfbox" -> {
                try (var pdf = org.apache.pdfbox.Loader.loadPDF(path.toFile())) {
                    yield pdf.getNumberOfPages();
                }
            }
            case "itextpdf" -> {
                var pdf = new com.itextpdf.text.pdf.PdfReader(path.toString());
                try { yield pdf.getNumberOfPages(); }
                finally { pdf.close(); }
            }
            case "openpdf" -> {
                var pdf = new org.openpdf.text.pdf.PdfReader(path.toString());
                try { yield pdf.getNumberOfPages(); }
                finally { pdf.close(); }
            }
            case "itext-kernel" -> {
                try (var pdf = new com.itextpdf.kernel.pdf.PdfDocument(
                        new com.itextpdf.kernel.pdf.PdfReader(path.toFile()))) {
                    yield pdf.getNumberOfPages();
                }
            }
            case "tika-pdf" -> {
                var metadata = new org.apache.tika.metadata.Metadata();
                metadata.set(org.apache.tika.metadata.HttpHeaders.CONTENT_TYPE, "application/pdf");
                try (var input = org.apache.tika.io.TikaInputStream.get(path)) {
                    new org.apache.tika.parser.pdf.PDFParser().parse(input,
                            new org.xml.sax.helpers.DefaultHandler(), metadata,
                            new org.apache.tika.parser.ParseContext());
                }
                var count = metadata.get("xmpTPg:NPages");
                if (count == null) count = metadata.get("Page-Count");
                if (count == null) throw new IllegalStateException("Tika page count missing");
                yield Integer.parseInt(count);
            }
            case "pdfjet" -> {
                try (var input = java.nio.file.Files.newInputStream(path)) {
                    var objects = new com.pdfjet.PDF().read(input);
                    var pagesObject = objects.stream()
                            .filter(object -> "/Pages".equals(object.getValue("/Type")))
                            .findFirst().orElseThrow();
                    yield Integer.parseInt(pagesObject.getValue("/Count"));
                }
            }
            case "icepdf-core" -> {
                var document = new org.icepdf.core.pobjects.Document();
                try {
                    document.setFile(path.toString());
                    yield document.getNumberOfPages();
                } finally {
                    document.dispose();
                }
            }
            case "pdfbox-preflight" -> {
                var parser = new org.apache.pdfbox.preflight.parser.PreflightParser(path.toFile());
                try (var document = parser.parse()) {
                    yield document.getNumberOfPages();
                }
            }
            case "openpdf-renderer" -> {
                var document = new org.openpdf.renderer.PDFFile(
                        java.nio.ByteBuffer.wrap(java.nio.file.Files.readAllBytes(path)));
                yield document.getNumPages();
            }
            case "verapdf-parser" -> {
                var document = new org.verapdf.pd.PDDocument(path.toString());
                try { yield document.getNumberOfPages(); }
                finally { document.close(); }
            }
            case "pdfviewfx" -> {
                var document = new com.dlsc.pdfviewfx.PDFBoxDocument(path.toFile());
                try { yield document.getNumberOfPages(); }
                finally { document.close(); }
            }
            case "sambox" -> {
                try (var document = org.sejda.sambox.input.PDFParser.parse(
                        org.sejda.io.SeekableSources.seekableSourceFrom(path.toFile()))) {
                    yield document.getNumberOfPages();
                }
            }
            case "swinglabs-pdf-renderer" -> new com.sun.pdfview.PDFFile(
                    java.nio.ByteBuffer.wrap(java.nio.file.Files.readAllBytes(path))).getNumPages();
            case "scireum-jpod" -> {
                var document = de.intarsys.pdf.pd.PDDocument.createFromLocator(
                        new de.intarsys.tools.locator.FileLocator(path.toFile()));
                try { yield document.getPageTree().getCount(); }
                finally { document.close(); }
            }
            case "tess4j-pdfbox" -> net.sourceforge.tess4j.util.PdfBoxUtilities.getPdfPageCount(path.toFile());
            default -> throw new IllegalArgumentException("unknown API: " + args[0]);
        };
        System.out.println("{\"pages\":" + pages + "}");
    }
}
