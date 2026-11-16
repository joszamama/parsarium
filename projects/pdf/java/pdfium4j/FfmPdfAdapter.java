package org.parsarium;

import java.nio.file.Path;

public final class FfmPdfAdapter {
    private FfmPdfAdapter() {}
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: FfmPdfAdapter CONTROL.pdf");
        Path path = Path.of(args[0]);
        int pages;
        try (var pdf = org.grimmory.pdfium4j.PdfDocument.open(path)) {
            pages = pdf.pageCount();
        }
        System.out.println("{\"pages\":" + pages + "}");
    }
}
