import fr.delthas.javamp3.Sound;
import java.io.BufferedInputStream;
import java.nio.file.Files;
import java.nio.file.Path;

/** Eligibility probe for the two existing valid, untagged Layer III controls. */
public final class Probe {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("one local MP3 file required");
        try (var input = new BufferedInputStream(Files.newInputStream(Path.of(args[0])));
             var sound = new Sound(input)) {
            long pcmBytes = 0;
            byte[] buffer = new byte[8192];
            for (int size; (size = sound.read(buffer)) != -1; ) pcmBytes += size;
            int channels = sound.isStereo() ? 2 : 1;
            if (pcmBytes % (2L * channels) != 0)
                throw new IllegalStateException("incomplete signed 16-bit PCM sample");
            System.out.printf("{\"sample_rate\":%d,\"channels\":%d,\"pcm_bytes\":%d,\"decoded_samples\":%d}%n",
                    sound.getSamplingFrequency(), channels, pcmBytes, pcmBytes / (2L * channels));
        }
    }
}
