package org.parsarium;

import ch.imagic.ffmpeg.FFprobe;
import java.io.File;
import java.nio.file.Path;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/** Parse a local tagged MP3 through the Imagic FFprobe wrapper's documented API. */
public final class ImagicMp3Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: ImagicMp3Adapter control.mp3");
        String bin = System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/opt/homebrew/bin");
        var workers = Executors.newCachedThreadPool();
        try {
            var ffprobe = new FFprobe(workers, Path.of(bin, "ffprobe").toFile());
            try (var job = ffprobe.probe(new File(args[0]))) {
                var result = job.get();
                var stream = result.getStreams().get(0);
                System.out.printf("{\"format\":\"%s\",\"codec\":\"%s\",\"frequency\":%d,\"channels\":%d,\"title\":\"%s\"}%n",
                    result.getFormat().getFormatName(), stream.getCodecName(),
                    stream.getSampleRate(), stream.getChannels(), result.getFormat().getTags().get("title"));
            }
        } finally {
            workers.shutdown();
            if (!workers.awaitTermination(10, TimeUnit.SECONDS)) throw new IllegalStateException("FFprobe workers did not stop");
        }
    }
}
