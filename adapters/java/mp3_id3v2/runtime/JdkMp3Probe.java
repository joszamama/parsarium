package org.parsarium;

import java.nio.file.Path;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.UnsupportedAudioFileException;

public final class JdkMp3Probe {
    private JdkMp3Probe() { }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) System.exit(2);
        try {
            var format = AudioSystem.getAudioFileFormat(Path.of(args[0]).toFile());
            System.out.printf("{\"recognized\":true,\"type\":\"%s\"}%n", format.getType());
        } catch (UnsupportedAudioFileException unsupported) {
            System.out.println("{\"recognized\":false,\"exception\":\"UnsupportedAudioFileException\"}");
        }
    }
}
