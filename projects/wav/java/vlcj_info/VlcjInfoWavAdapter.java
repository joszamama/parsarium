package org.parsarium;

import uk.co.caprica.vlcjinfo.MediaInfoFile;

/** Query WAV fields parsed by libmediainfo through vlcj-info's local-file API. */
public final class VlcjInfoWavAdapter {
    public static void main(String[] args) {
        if (args.length != 1) throw new IllegalArgumentException("usage: VlcjInfoWavAdapter control.wav");
        var info = new MediaInfoFile(args[0]);
        if (!info.open()) throw new IllegalStateException("MediaInfo could not open local WAV");
        try {
            String format = info.info("General;%Format%");
            int sampleRate = Integer.parseInt(info.info("Audio;%SamplingRate%"));
            int channels = Integer.parseInt(info.info("Audio;%Channels%"));
            System.out.printf("{\"format\":\"%s\",\"sample_rate\":%d,\"channels\":%d}%n",
                format, sampleRate, channels);
        } finally {
            info.close();
        }
    }
}
