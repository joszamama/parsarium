import java.nio.file.Files;
import java.nio.file.Path;
import org.jaudiotagger.audio.exceptions.InvalidAudioFrameException;

public final class GenericHarness {
    public static void fuzzerTestOneInput(byte[] data) {
        try {
            org.parsarium.Mp3Adapter.parse(data);
        } catch (InvalidAudioFrameException | IllegalArgumentException ignored) {
            // The documented frame-header API reports expected parse failures.
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one local input path required");
        System.out.println(org.parsarium.Mp3Adapter.parse(Files.readAllBytes(Path.of(args[0]))));
    }
}
