package org.parsarium;

import java.nio.file.Path;
import com.github.kokorin.jaffree.ffprobe.FFprobe;

/** Parse the supplied local ASCII PNM through Jaffree and a pinned FFprobe executable. */
public final class JaffreePnmAdapter {
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("usage: JaffreePnmAdapter control.ppm");
        String bin = System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/opt/homebrew/bin");
        var result = FFprobe.atPath(Path.of(bin)).setShowStreams(true).setInput(Path.of(args[0])).execute();
        var streams = result.getStreams();
        if (streams.size() != 1) throw new IllegalStateException("expected one PPM stream");
        var video = streams.get(0);
        System.out.printf("{\"codec\":\"%s\",\"width\":%d,\"height\":%d}%n",
            video.getCodecName(), video.getWidth(), video.getHeight());
    }
}
