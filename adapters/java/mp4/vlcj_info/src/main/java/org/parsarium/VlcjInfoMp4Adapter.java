package org.parsarium;

import uk.co.caprica.vlcjinfo.MediaInfoFile;

/** Parse the local MP4 through vlcj-info and libmediainfo. */
public final class VlcjInfoMp4Adapter {
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("usage: VlcjInfoMp4Adapter control.mp4");
        var info = new MediaInfoFile(args[0]);
        if (!info.open()) throw new IllegalStateException("MediaInfo could not open local MP4");
        try {
            String format = info.info("General;%Format%");
            int width = Integer.parseInt(info.info("Video;%Width%"));
            int height = Integer.parseInt(info.info("Video;%Height%"));
            int sampleRate = Integer.parseInt(info.info("Audio;%SamplingRate%"));
            System.out.printf("{\"format\":\"%s\",\"width\":%d,\"height\":%d,\"sample_rate\":%d}%n",
                format, width, height, sampleRate);
        } finally {
            info.close();
        }
    }
}
