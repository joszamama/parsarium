package org.parsarium;

import java.io.File;
import ws.schild.jave.MultimediaObject;

/** JAVE2 reads the local control through its pinned bundled FFmpeg executable. */
public final class JaveWavAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: JaveWavAdapter control.wav");
        var info = new MultimediaObject(new File(args[0])).getInfo();
        var audio = info.getAudio();
        System.out.printf("{\"format\":\"%s\",\"codec\":\"%s\",\"sample_rate\":%d,\"channels\":%d}%n",
            info.getFormat(), audio.getDecoder(), audio.getSamplingRate(), audio.getChannels());
    }
}
