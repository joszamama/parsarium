package org.parsarium;

import java.io.RandomAccessFile;
import net.sourceforge.jaad.mp4.MP4Container;
import net.sourceforge.jaad.mp4.api.AudioTrack;

/** Parse the local MP4 with the pinned JAAD demultiplexer. */
public final class JaadMp4Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: JaadMp4Adapter control.mp4");
        try (var file = new RandomAccessFile(args[0], "r")) {
            var movie = new MP4Container(file).getMovie();
            var audio = movie.getTracks().stream().filter(AudioTrack.class::isInstance)
                .map(AudioTrack.class::cast).findFirst().orElseThrow();
            System.out.printf("{\"tracks\":%d,\"audio_codec\":\"%s\",\"sample_rate\":%d,\"channels\":%d}%n",
                movie.getTracks().size(), audio.getCodec(), audio.getSampleRate(), audio.getChannelCount());
        }
    }
}
