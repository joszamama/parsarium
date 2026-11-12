package org.parsarium;

import java.nio.file.Path;

public final class JPodOriginalAdapter {
    private JPodOriginalAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: JPodOriginalAdapter CONTROL.pdf");
        var document = de.intarsys.pdf.pd.PDDocument.createFromLocator(
                new de.intarsys.tools.locator.FileLocator(Path.of(args[0]).toFile()));
        try {
            System.out.println("{\"pages\":" + document.getPageTree().getCount() + "}");
        } finally {
            document.close();
        }
    }
}
