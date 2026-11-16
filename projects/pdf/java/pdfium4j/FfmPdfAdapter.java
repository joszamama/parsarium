package org.parsarium;

import java.nio.file.Path;

public final class FfmPdfAdapter {
    private FfmPdfAdapter() {}
    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("usage: FfmPdfAdapter API CONTROL.pdf");
        Path path = Path.of(args[1]);
        int pages = switch (args[0]) {
            case "pdfium4j" -> {
                try (var pdf = org.grimmory.pdfium4j.PdfDocument.open(path)) {
                    yield pdf.pageCount();
                }
            }
            default -> throw new IllegalArgumentException("unknown API: " + args[0]);
        };
        System.out.println("{\"pages\":" + pages + "}");
    }
}
