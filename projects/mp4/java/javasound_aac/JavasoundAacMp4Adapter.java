package org.parsarium;

import java.io.RandomAccessFile;
import java.util.StringJoiner;
import net.sourceforge.jaad.mp4.MP4Container;
import net.sourceforge.jaad.mp4.MP4InputStream;
import net.sourceforge.jaad.mp4.api.AudioTrack;

/** Parse the local MP4 with the pinned Java Sound AAC distribution of JAAD. */
public final class JavasoundAacMp4Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: JavasoundAacMp4Adapter control.mp4");
        try (var file = new RandomAccessFile(args[0], "r");
             var input = MP4InputStream.open(file)) {
            var movie = new MP4Container(input).getMovie();
            var fields = new StringJoiner(",", "{", "}");
            fields.add("\"tracks\":" + movie.getTracks().size());
            movie.getTracks().stream().filter(AudioTrack.class::isInstance)
                .map(AudioTrack.class::cast).findFirst().ifPresent(audio -> {
                    fields.add("\"audio_codec\":" + (audio.getCodec() == null ? "null" : "\"" + audio.getCodec() + "\""));
                    fields.add("\"sample_rate\":" + audio.getSampleRate());
                    fields.add("\"channels\":" + audio.getChannelCount());
                });
            System.out.println(fields);
        }
    }
}
