package org.parsarium;

import java.nio.file.Path;
import net.bramp.ffmpeg.FFprobe;

/** Parse a local WAV via bramp's documented FFprobe wrapper API. */
public final class BrampWavAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: BrampWavAdapter control.wav");
        String bin = System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/opt/homebrew/bin");
        var result = new FFprobe(Path.of(bin, "ffprobe").toString()).probe(args[0]);
        var stream = result.getStreams().get(0);
        System.out.printf("{\"format\":\"%s\",\"codec\":\"%s\",\"sample_rate\":%d,\"channels\":%d}%n",
            result.getFormat().getFormatName(), stream.getCodecName(),
            stream.getSampleRate(), stream.getChannels());
    }
}
