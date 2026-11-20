import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.jaudiotagger.audio.AudioFileIO;
import org.jaudiotagger.audio.mp3.MP3File;
import org.jaudiotagger.tag.FieldKey;

public final class JaudiotaggerHarness {
    record Parsed(String title, String artist, String album) {}

    /** JSON string literal; non-ASCII characters are written as \\uXXXX escapes. */
    static String quote(String value) {
        StringBuilder out = new StringBuilder("\"");
        for (char c : value.toCharArray()) {
            if (c == '"' || c == '\\') out.append('\\').append(c);
            else if (c < 0x20 || c > 0x7e) out.append(String.format("\\u%04x", (int) c));
            else out.append(c);
        }
        return out.append('"').toString();
    }

    /** JSON object of the non-null values, in the given key order. */
    static String object(Object... pairs) {
        StringBuilder out = new StringBuilder("{");
        for (int i = 0; i < pairs.length; i += 2) {
            if (pairs[i + 1] == null) continue;
            if (out.length() > 1) out.append(',');
            Object value = pairs[i + 1];
            out.append(quote((String) pairs[i])).append(':')
               .append(value instanceof String text ? quote(text) : String.valueOf(value));
        }
        return out.append('}').toString();
    }
    static Parsed parse(byte[] data) throws Exception {
        if (data.length == 0 || data.length > (1 << 20)) throw new IOException("input outside harness limit");
        Path path = Files.createTempFile("parsarium-mp3-", ".mp3");
        try {
            Files.write(path, data);
            var audio = AudioFileIO.read(path.toFile());
            if (!(audio instanceof MP3File mp3)) throw new IOException("not read as an MP3 file");
            if (!mp3.hasID3v2Tag()) return null;
            var tag = mp3.getID3v2Tag();
            return new Parsed(tag.getFirst(FieldKey.TITLE), tag.getFirst(FieldKey.ARTIST),
                              tag.getFirst(FieldKey.ALBUM));
        } finally { Files.deleteIfExists(path); }
    }
    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); } catch (Exception ignored) { }
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected control path");
        java.util.logging.Logger.getLogger("org.jaudiotagger").setLevel(java.util.logging.Level.OFF);
        Parsed p = parse(Files.readAllBytes(Path.of(args[0])));
        System.out.println(p == null ? "{}" : object("title", p.title(), "artist", p.artist(), "album", p.album()));
    }
}
