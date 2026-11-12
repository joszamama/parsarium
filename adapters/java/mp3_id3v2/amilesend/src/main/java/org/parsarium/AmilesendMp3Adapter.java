package org.parsarium;

import com.amilesend.mediainfo.MediaInfo;
import com.amilesend.mediainfo.lib.MediaInfoAccessor;
import com.amilesend.mediainfo.lib.MediaInfoLibrary;
import com.amilesend.mediainfo.type.StreamType;
import java.io.File;

/** Parse the local tagged MP3 through the documented MediaInfo JNA wrapper. */
public final class AmilesendMp3Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: AmilesendMp3Adapter control.mp3");
        var library = MediaInfoLibrary.newInstance();
        var accessor = new MediaInfoAccessor(library);
        try (var info = new MediaInfo(accessor).open(new File(args[0]))) {
            String format = info.get(StreamType.General, 0, "Format");
            String title = info.get(StreamType.General, 0, "Title");
            int sampleRate = Integer.parseInt(info.get(StreamType.Audio, 0, "SamplingRate"));
            int channels = Integer.parseInt(info.get(StreamType.Audio, 0, "Channels"));
            System.out.printf("{\"format\":\"%s\",\"frequency\":%d,\"channels\":%d,\"title\":\"%s\"}%n",
                format, sampleRate, channels, title);
        }
    }
}
