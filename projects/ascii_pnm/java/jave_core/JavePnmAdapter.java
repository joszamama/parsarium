package org.parsarium;

import java.io.File;
import ws.schild.jave.MultimediaObject;

/** Parse a local ASCII PPM through JAVE2 and its pinned FFmpeg executable. */
public final class JavePnmAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: JavePnmAdapter control.ppm");
        var info = new MultimediaObject(new File(args[0])).getInfo();
        var video = info.getVideo();
        if (video == null) throw new IllegalStateException("no PPM video stream");
        System.out.printf("{\"format\":\"%s\",\"width\":%d,\"height\":%d}%n",
            info.getFormat(), video.getSize().getWidth(), video.getSize().getHeight());
    }
}
