package org.parsarium;

import ch.imagic.ffmpeg.FFprobe;
import java.io.File;
import java.nio.file.Path;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/** Parse the supplied local MP4 through Imagic's FFprobe wrapper. */
public final class ImagicMp4Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: ImagicMp4Adapter control.mp4");
        String bin = System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/usr/bin");
        var workers = Executors.newCachedThreadPool();
        try {
            var ffprobe = new FFprobe(workers, Path.of(bin, "ffprobe").toFile());
            try (var job = ffprobe.probe(new File(args[0]))) {
                var result = job.get();
                var streams = result.getStreams();
                if (streams.size() != 2) throw new IllegalStateException("expected two streams");
                var video = streams.get(0);
                var audio = streams.get(1);
                System.out.printf("{\"format\":\"%s\",\"video_codec\":\"%s\",\"width\":%d,\"height\":%d,\"audio_codec\":\"%s\",\"sample_rate\":%d}%n",
                    result.getFormat().getFormatName(), video.getCodecName(), video.getWidth(), video.getHeight(),
                    audio.getCodecName(), audio.getSampleRate());
            }
        } finally {
            workers.shutdown();
            if (!workers.awaitTermination(10, TimeUnit.SECONDS)) throw new IllegalStateException("FFprobe workers did not stop");
        }
    }
}
