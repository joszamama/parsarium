import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.nio.channels.Channels;
import java.nio.file.Files;
import java.nio.file.Path;
import org.jcodec.codecs.wav.WavInput;

public final class JcodecHarness {
    record Parsed(int sampleRate, int channels, int bits) {}

    static Parsed parse(byte[] data) throws IOException {
        if (data.length == 0 || data.length > (1 << 20)) {
            throw new IOException("input outside harness limit");
        }
        try (var reader = new WavInput(Channels.newChannel(new ByteArrayInputStream(data)))) {
            var format = reader.getFormat();
            return new Parsed(format.getSampleRate(), format.getChannels(),
                              format.getSampleSizeInBits());
        }
    }

    public static void fuzzerTestOneInput(byte[] data) {
        try {
            parse(data);
        } catch (IOException | IllegalArgumentException ignored) {
            // Invalid inputs may be rejected by the documented reader.
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("expected control path");
        Parsed result = parse(Files.readAllBytes(Path.of(args[0])));
        System.out.printf("{\"sample_rate\":%d,\"channels\":%d,\"bits\":%d}%n",
                result.sampleRate(), result.channels(), result.bits());
    }
}
