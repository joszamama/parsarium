package org.parsarium;

import java.nio.file.Path;
import com.github.kokorin.jaffree.ffprobe.FFprobe;

/** Parse the supplied local MP4 through the v47 Jaffree fork. */
public final class V47Mp4Adapter {
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("usage: V47Mp4Adapter control.mp4");
        String bin = System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/opt/homebrew/bin");
        var result = FFprobe.atPath(Path.of(bin)).setShowStreams(true).setInput(Path.of(args[0])).execute();
        var streams = result.getStreams();
        if (streams.size() != 2) throw new IllegalStateException("expected two streams");
        var video = streams.get(0);
        var audio = streams.get(1);
        System.out.printf("{\"video_codec\":\"%s\",\"width\":%d,\"height\":%d,\"audio_codec\":\"%s\",\"sample_rate\":%d}%n",
            video.getCodecName(), video.getWidth(), video.getHeight(),
            audio.getCodecName(), audio.getSampleRate());
    }
}
