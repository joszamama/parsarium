package org.parsarium;

import java.io.File;
import java.util.StringJoiner;
import ws.schild.jave.MultimediaObject;

/** Parse the supplied local MP4 through JAVE2 and its pinned FFmpeg executable. */
public final class JaveMp4Adapter {
    private static String text(String value) {
        return value == null ? "null" : "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: JaveMp4Adapter control.mp4");
        var info = new MultimediaObject(new File(args[0])).getInfo();
        var video = info.getVideo();
        var audio = info.getAudio();
        var fields = new StringJoiner(",", "{", "}");
        fields.add("\"format\":" + text(info.getFormat()));
        if (video != null && video.getSize() != null) {
            fields.add("\"width\":" + video.getSize().getWidth());
            fields.add("\"height\":" + video.getSize().getHeight());
        }
        if (audio != null) {
            fields.add("\"sample_rate\":" + audio.getSamplingRate());
            fields.add("\"channels\":" + audio.getChannels());
        }
        System.out.println(fields);
    }
}
