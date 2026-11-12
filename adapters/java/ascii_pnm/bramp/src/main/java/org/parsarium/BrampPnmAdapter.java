package org.parsarium;

import java.nio.file.Path;
import net.bramp.ffmpeg.FFprobe;

/** Parse the supplied local ASCII PNM through bramp's FFprobe wrapper. */
public final class BrampPnmAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: BrampPnmAdapter control.ppm");
        String bin = System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/opt/homebrew/bin");
        var result = new FFprobe(Path.of(bin, "ffprobe").toString()).probe(args[0]);
        var streams = result.getStreams();
        if (streams.size() != 1) throw new IllegalStateException("expected one PPM stream");
        var video = streams.get(0);
        System.out.printf("{\"codec\":\"%s\",\"width\":%d,\"height\":%d}%n",
            video.getCodecName(), video.getWidth(), video.getHeight());
    }
}
