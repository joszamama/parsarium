import com.mpatric.mp3agic.InvalidDataException;
import com.mpatric.mp3agic.UnsupportedTagException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public final class GenericHarness {
    public static void fuzzerTestOneInput(byte[] data) {
        if (data.length == 0 || data.length > (1 << 20)) return;
        Path input = null;
        try {
            input = Files.createTempFile("parsarium-mp3agic-", ".mp3");
            Files.write(input, data);
            org.parsarium.Mp3Adapter.parse(input);
        } catch (IOException | InvalidDataException | UnsupportedTagException | IllegalArgumentException ignored) {
            // The local-file API reports expected parse failures.
        } finally {
            if (input != null) {
                try { Files.deleteIfExists(input); } catch (IOException ignored) { }
            }
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one local input path required");
        System.out.println(org.parsarium.Mp3Adapter.parse(Path.of(args[0])));
    }
}
