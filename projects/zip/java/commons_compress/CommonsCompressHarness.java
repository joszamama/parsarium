import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Base64;
import java.util.Enumeration;
import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
import org.apache.commons.compress.archivers.zip.ZipFile;
import org.apache.commons.compress.utils.SeekableInMemoryByteChannel;

public final class CommonsCompressHarness {
    record Parsed(String name, String contentBase64) {}

    static Parsed parse(byte[] data) throws IOException {
        if (data.length == 0 || data.length > (1 << 20)) {
            throw new IOException("input outside harness limit");
        }
        try (var channel = new SeekableInMemoryByteChannel(data);
             var archive = ZipFile.builder().setSeekableByteChannel(channel).get()) {
            Enumeration<ZipArchiveEntry> entries = archive.getEntries();
            if (!entries.hasMoreElements()) throw new IOException("no ZIP entries");
            ZipArchiveEntry entry = entries.nextElement();
            if (entry.getSize() > (1 << 20)) throw new IOException("entry outside harness limit");
            try (InputStream stream = archive.getInputStream(entry)) {
                byte[] content = stream.readNBytes((1 << 20) + 1);
                if (content.length > (1 << 20)) throw new IOException("entry outside harness limit");
                return new Parsed(entry.getName(), Base64.getEncoder().encodeToString(content));
            }
        }
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try {
            parse(data);
        } catch (IOException | IllegalArgumentException ignored) {
            // Invalid archives can be rejected by the documented parser API.
        }
    }

    private static String jsonString(String text) {
        StringBuilder out = new StringBuilder("\"");
        for (int i = 0; i < text.length(); i++) {
            char ch = text.charAt(i);
            if (ch == '"' || ch == '\\') out.append('\\').append(ch);
            else if (ch < 0x20) out.append(String.format("\\u%04x", (int) ch));
            else out.append(ch);
        }
        return out.append('"').toString();
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected control path");
        Parsed result = parse(Files.readAllBytes(Path.of(args[0])));
        System.out.printf("{\"name\":%s,\"content_base64\":%s}%n",
                jsonString(result.name()), jsonString(result.contentBase64()));
    }
}
