package org.parsarium;

import java.io.FileInputStream;
import net.sourceforge.jaad.mp4.MP4Container;
import net.sourceforge.jaad.mp4.MP4InputStream;
import net.sourceforge.jaad.mp4.api.AudioTrack;

/** Parse the local MP4 with the pinned Java Sound AAC distribution of JAAD. */
public final class JavasoundAacMp4Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: JavasoundAacMp4Adapter control.mp4");
        try (var file = new FileInputStream(args[0]);
             var input = MP4InputStream.open(file)) {
            var movie = new MP4Container(input).getMovie();
            var audio = movie.getTracks().stream().filter(AudioTrack.class::isInstance)
                .map(AudioTrack.class::cast).findFirst().orElseThrow();
            System.out.printf("{\"tracks\":%d,\"audio_codec\":\"%s\",\"sample_rate\":%d,\"channels\":%d}%n",
                movie.getTracks().size(), audio.getCodec(), audio.getSampleRate(), audio.getChannelCount());
        }
    }
}
