import java.nio.file.Files;
import java.nio.file.Path;

public final class GenericHarness {
    public static void fuzzerTestOneInput(byte[] data) {
        if (data.length == 0 || data.length > (1 << 20)) return;
        try {
            org.parsarium.Mp3SpiAdapter.parse(data);
        } catch (javax.sound.sampled.UnsupportedAudioFileException | java.io.IOException |
                 IllegalArgumentException ignored) {
            // Expected parse failures are reported by the Java Sound API.
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one local input path required");
        System.out.println(org.parsarium.Mp3SpiAdapter.parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
