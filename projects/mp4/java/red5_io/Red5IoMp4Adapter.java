package org.parsarium;

import java.io.File;
import org.red5.io.mp4.impl.MP4Reader;

/** Parse the local MP4 through Red5's MP4Reader package API. */
public final class Red5IoMp4Adapter {
    private static String text(String value) {
        return value == null ? "null" : "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: Red5IoMp4Adapter control.mp4");
        var reader = new MP4Reader(new File(args[0]));
        try {
            var frames = reader.analyzeKeyFrames();
            System.out.printf("{\"video\":%s,\"keyframes\":%d,\"video_codec\":%s,\"audio_codec\":%s}%n",
                reader.hasVideo(), frames.positions.length,
                text(reader.getVideoCodecId()), text(reader.getAudioCodecId()));
        } finally {
            reader.close();
        }
    }
}
