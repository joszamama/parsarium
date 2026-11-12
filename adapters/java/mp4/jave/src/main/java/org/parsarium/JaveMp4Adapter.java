package org.parsarium;

import java.io.File;
import ws.schild.jave.MultimediaObject;

/** Parse the supplied local MP4 through JAVE2 and its pinned FFmpeg executable. */
public final class JaveMp4Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: JaveMp4Adapter control.mp4");
        var info = new MultimediaObject(new File(args[0])).getInfo();
        var video = info.getVideo();
        var audio = info.getAudio();
        if (video == null || audio == null) throw new IllegalStateException("missing MP4 streams");
        System.out.printf("{\"format\":\"%s\",\"width\":%d,\"height\":%d,\"sample_rate\":%d,\"channels\":%d}%n",
            info.getFormat(), video.getSize().getWidth(), video.getSize().getHeight(),
            audio.getSamplingRate(), audio.getChannels());
    }
}
