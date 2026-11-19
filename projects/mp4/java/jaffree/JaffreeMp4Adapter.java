package org.parsarium;

import java.nio.file.Path;
import java.util.StringJoiner;
import com.github.kokorin.jaffree.StreamType;
import com.github.kokorin.jaffree.ffprobe.FFprobe;

/** Parse the supplied local MP4 through Jaffree and a pinned FFprobe executable. */
public final class JaffreeMp4Adapter {
    private static String text(String value) {
        return value == null ? "null" : "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
    }

    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("usage: JaffreeMp4Adapter control.mp4");
        String bin = System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/usr/bin");
        var result = FFprobe.atPath(Path.of(bin)).setShowStreams(true).setInput(Path.of(args[0])).execute();
        var streams = result.getStreams();
        var video = streams.stream().filter(stream -> stream.getCodecType() == StreamType.VIDEO).findFirst();
        var audio = streams.stream().filter(stream -> stream.getCodecType() == StreamType.AUDIO).findFirst();
        var fields = new StringJoiner(",", "{", "}");
        video.ifPresent(stream -> {
            fields.add("\"video_codec\":" + text(stream.getCodecName()));
            fields.add("\"width\":" + stream.getWidth());
            fields.add("\"height\":" + stream.getHeight());
        });
        audio.ifPresent(stream -> {
            fields.add("\"audio_codec\":" + text(stream.getCodecName()));
            fields.add("\"sample_rate\":" + stream.getSampleRate());
        });
        System.out.println(fields);
    }
}
