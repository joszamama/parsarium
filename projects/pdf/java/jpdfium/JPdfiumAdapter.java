package org.parsarium;

import java.nio.file.Path;

public final class JPdfiumAdapter {
    private JPdfiumAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: JPdfiumAdapter CONTROL.pdf");
        try (var document = stirling.software.jpdfium.PdfDocument.open(Path.of(args[0]))) {
            System.out.println("{\"pages\":" + document.pageCount() + "}");
        }
    }
}
