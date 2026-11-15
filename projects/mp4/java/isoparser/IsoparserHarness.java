import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.mp4parser.IsoFile;

public final class IsoparserHarness {
    record Parsed(int tracks, long timescale) {}
    static Parsed parse(byte[] data) throws IOException {
        if (data.length == 0 || data.length > (1 << 20)) throw new IOException("input outside harness limit");
        Path path = Files.createTempFile("parsarium-mp4-", ".mp4");
        try {
            Files.write(path, data);
            try (var iso = new IsoFile(path.toFile())) {
                var movie = iso.getMovieBox();
                if (movie == null) throw new IOException("no moov box");
                return new Parsed(movie.getTrackCount(), movie.getMovieHeaderBox().getTimescale());
            }
        } finally { Files.deleteIfExists(path); }
    }
    public static void fuzzerTestOneInput(byte[] data) {
        try { parse(data); } catch (IOException | IllegalArgumentException ignored) { }
    }
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected control path");
        Parsed p = parse(Files.readAllBytes(Path.of(args[0])));
        System.out.printf("{\"tracks\":%d,\"timescale\":%d}%n", p.tracks(), p.timescale());
    }
}
