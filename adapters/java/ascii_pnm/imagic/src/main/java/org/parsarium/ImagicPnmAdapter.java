package org.parsarium;

import ch.imagic.ffmpeg.FFprobe;
import java.io.File;
import java.nio.file.Path;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/** Parse the supplied local ASCII PNM through Imagic's FFprobe wrapper. */
public final class ImagicPnmAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: ImagicPnmAdapter control.ppm");
        String bin = System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/opt/homebrew/bin");
        var workers = Executors.newCachedThreadPool();
        try {
            var ffprobe = new FFprobe(workers, Path.of(bin, "ffprobe").toFile());
            try (var job = ffprobe.probe(new File(args[0]))) {
                var result = job.get();
                var streams = result.getStreams();
                if (streams.size() != 1) throw new IllegalStateException("expected one PPM stream");
                var video = streams.get(0);
                System.out.printf("{\"codec\":\"%s\",\"width\":%d,\"height\":%d}%n",
                    video.getCodecName(), video.getWidth(), video.getHeight());
            }
        } finally {
            workers.shutdown();
            if (!workers.awaitTermination(10, TimeUnit.SECONDS)) throw new IllegalStateException("FFprobe workers did not stop");
        }
    }
}
