import java.io.File;
import javax.imageio.ImageIO;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.UnsupportedAudioFileException;

/** Probe only documented JDK reader families on a valid MP4, without dependencies. */
public final class JdkMp4Probe {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: JdkMp4Probe control.mp4");
        File file = new File(args[0]);
        boolean image = ImageIO.read(file) != null;
        boolean audio;
        try {
            AudioSystem.getAudioFileFormat(file);
            audio = true;
        } catch (UnsupportedAudioFileException expected) {
            audio = false;
        }
        System.out.printf("{\"imageio_reader\":%s,\"audio_system_reader\":%s}%n", image, audio);
    }
}
