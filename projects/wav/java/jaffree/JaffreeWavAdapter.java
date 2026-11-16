package org.parsarium;

import java.nio.file.Path;
import com.github.kokorin.jaffree.ffprobe.FFprobe;

/** Jaffree's local-file API invokes the pinned local ffprobe executable. */
public final class JaffreeWavAdapter {
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("usage: JaffreeWavAdapter control.wav");
        String bin = System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/usr/bin");
        var result = FFprobe.atPath(Path.of(bin)).setShowStreams(true).setInput(Path.of(args[0])).execute();
        var audio = result.getStreams().get(0);
        System.out.printf("{\"codec\":\"%s\",\"sample_rate\":%d,\"channels\":%d}%n",
            audio.getCodecName(), audio.getSampleRate(), audio.getChannels());
    }
}
