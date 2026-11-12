package org.parsarium;

import uk.co.caprica.vlcjinfo.MediaInfoFile;

/** Query tagged MP3 fields parsed by libmediainfo through vlcj-info's local-file API. */
public final class VlcjInfoMp3Adapter {
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("usage: VlcjInfoMp3Adapter control.mp3");
        var info = new MediaInfoFile(args[0]);
        if (!info.open()) throw new IllegalStateException("MediaInfo could not open local tagged MP3");
        try {
            String format = info.info("General;%Format%");
            String title = info.info("General;%Title%");
            int sampleRate = Integer.parseInt(info.info("Audio;%SamplingRate%"));
            int channels = Integer.parseInt(info.info("Audio;%Channels%"));
            System.out.printf("{\"format\":\"%s\",\"frequency\":%d,\"channels\":%d,\"title\":\"%s\"}%n",
                format, sampleRate, channels, title);
        } finally {
            info.close();
        }
    }
}
