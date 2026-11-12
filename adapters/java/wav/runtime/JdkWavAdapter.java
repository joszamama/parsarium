import java.io.File;
import javax.sound.sampled.AudioFileFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;

/** Compile and run without a third-party classpath to prove JDK-bundled parsing. */
public final class JdkWavAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("usage: JdkWavAdapter mode control.wav");
        File file = new File(args[1]);
        switch (args[0]) {
            case "audio_file_format" -> {
                AudioFileFormat format = AudioSystem.getAudioFileFormat(file);
                System.out.printf("{\"type\":\"%s\",\"sample_rate\":%d,\"channels\":%d,\"frames\":%d}%n",
                    format.getType(), (int) format.getFormat().getSampleRate(),
                    format.getFormat().getChannels(), format.getFrameLength());
            }
            case "audio_input_stream" -> {
                try (AudioInputStream stream = AudioSystem.getAudioInputStream(file)) {
                    byte[] sample = stream.readNBytes(8);
                    System.out.printf("{\"sample_rate\":%d,\"channels\":%d,\"frames\":%d,\"sample_bytes\":%d}%n",
                        (int) stream.getFormat().getSampleRate(), stream.getFormat().getChannels(),
                        stream.getFrameLength(), sample.length);
                }
            }
            default -> throw new IllegalArgumentException("unknown mode: " + args[0]);
        }
    }
}
