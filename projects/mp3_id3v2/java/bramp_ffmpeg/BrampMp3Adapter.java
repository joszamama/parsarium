package org.parsarium;

import java.nio.file.Path;
import net.bramp.ffmpeg.FFprobe;

/** Parse a local tagged MP3 via bramp's documented FFprobe wrapper API. */
public final class BrampMp3Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: BrampMp3Adapter control.mp3");
        String bin = System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/usr/bin");
        var result = new FFprobe(Path.of(bin, "ffprobe").toString()).probe(args[0]);
        var stream = result.getStreams().get(0);
        System.out.printf("{\"format\":\"%s\",\"codec\":\"%s\",\"frequency\":%d,\"channels\":%d,\"title\":\"%s\"}%n",
            result.getFormat().getFormatName(), stream.getCodecName(),
            stream.getSampleRate(), stream.getChannels(), result.getFormat().getTags().get("title"));
    }
}
