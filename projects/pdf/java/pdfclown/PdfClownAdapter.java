package org.parsarium;

public final class PdfClownAdapter {
    private PdfClownAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: PdfClownAdapter CONTROL.pdf");
        try (var file = new org.pdfclown.files.File(args[0])) {
            System.out.println("{\"pages\":" + file.getDocument().getPages().size() + "}");
        }
    }
}
