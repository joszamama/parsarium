package org.parsarium;

import java.nio.file.Path;

public final class IcePdf8Adapter {
    private IcePdf8Adapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: IcePdf8Adapter CONTROL.pdf");
        Path path = Path.of(args[0]);
        var document = new org.icepdf.core.pobjects.Document();
        try {
            document.setFile(path.toString());
            System.out.println("{\"pages\":" + document.getNumberOfPages() + "}");
        } finally {
            document.dispose();
        }
    }
}
