import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.apache.pdfbox.Loader;

public final class PdfboxHarness {
    static int parse(byte[] data) throws IOException {
        if (data.length == 0 || data.length > (1 << 20)) throw new IOException("input outside harness limit");
        Path path = Files.createTempFile("parsarium-pdf-", ".pdf");
        try {
            Files.write(path, data);
            try (var document = Loader.loadPDF(path.toFile())) {
                return document.getNumberOfPages();
            }
        } finally { Files.deleteIfExists(path); }
    }
    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); } catch (IOException | IllegalArgumentException ignored) { }
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected control path");
        System.out.printf("{\"pages\":%d}%n", parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
