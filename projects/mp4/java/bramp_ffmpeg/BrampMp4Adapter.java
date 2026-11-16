package org.parsarium;

import java.nio.file.Path;
import net.bramp.ffmpeg.FFprobe;

/** Parse the supplied local MP4 through bramp's FFprobe wrapper. */
public final class BrampMp4Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: BrampMp4Adapter control.mp4");
        String bin = System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/usr/bin");
        var result = new FFprobe(Path.of(bin, "ffprobe").toString()).probe(args[0]);
        var streams = result.getStreams();
        if (streams.size() != 2) throw new IllegalStateException("expected two streams");
        var video = streams.get(0);
        var audio = streams.get(1);
        System.out.printf("{\"format\":\"%s\",\"video_codec\":\"%s\",\"width\":%d,\"height\":%d,\"audio_codec\":\"%s\",\"sample_rate\":%d}%n",
            result.getFormat().getFormatName(), video.getCodecName(), video.getWidth(), video.getHeight(),
            audio.getCodecName(), audio.getSampleRate());
    }
}
