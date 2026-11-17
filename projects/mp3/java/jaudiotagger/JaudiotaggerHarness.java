import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.jaudiotagger.audio.AudioFileIO;
import org.jaudiotagger.audio.mp3.MP3File;
import org.jaudiotagger.tag.FieldKey;

public final class JaudiotaggerHarness {
    record Parsed(String title, String artist, String album) {}
    static Parsed parse(byte[] data) throws Exception {
        if (data.length == 0 || data.length > (1 << 20)) throw new IOException("input outside harness limit");
        Path path = Files.createTempFile("parsarium-mp3-", ".mp3");
        try {
            Files.write(path, data);
            var audio = AudioFileIO.read(path.toFile());
            if (!(audio instanceof MP3File mp3) || !mp3.hasID3v2Tag()) {
                throw new IOException("no MP3 ID3v2 tag");
            }
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
        System.out.printf("{\"title\":\"%s\",\"artist\":\"%s\",\"album\":\"%s\"}%n",
                          p.title(), p.artist(), p.album());
    }
}
