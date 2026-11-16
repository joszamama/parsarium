package org.parsarium;

import java.nio.file.Path;
import com.github.kokorin.jaffree.ffprobe.FFprobe;

/** Parse a local tagged MP3 through the v47 Jaffree fork's FFprobe API. */
public final class V47Mp3Adapter {
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("usage: V47Mp3Adapter control.mp3");
        String bin = System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/usr/bin");
        var result = FFprobe.atPath(Path.of(bin)).setShowStreams(true).setShowFormat(true).setInput(Path.of(args[0])).execute();
        var audio = result.getStreams().get(0);
        System.out.printf("{\"codec\":\"%s\",\"frequency\":%d,\"channels\":%d,\"title\":\"%s\"}%n",
            audio.getCodecName(), audio.getSampleRate(), audio.getChannels(), result.getFormat().getTag("title"));
    }
}
