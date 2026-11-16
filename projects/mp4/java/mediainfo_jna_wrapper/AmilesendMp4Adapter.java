package org.parsarium;

import com.amilesend.mediainfo.MediaInfo;
import com.amilesend.mediainfo.lib.MediaInfoAccessor;
import com.amilesend.mediainfo.lib.MediaInfoLibrary;
import com.amilesend.mediainfo.type.StreamType;
import java.io.File;

/** Parse the padded local MP4 through the MediaInfo JNA wrapper. */
public final class AmilesendMp4Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: AmilesendMp4Adapter control.mp4");
        var library = MediaInfoLibrary.newInstance();
        var accessor = new MediaInfoAccessor(library);
        try (var info = new MediaInfo(accessor).open(new File(args[0]))) {
            String format = info.get(StreamType.General, 0, "Format");
            int width = Integer.parseInt(info.get(StreamType.Video, 0, "Width"));
            int height = Integer.parseInt(info.get(StreamType.Video, 0, "Height"));
            int sampleRate = Integer.parseInt(info.get(StreamType.Audio, 0, "SamplingRate"));
            System.out.printf("{\"format\":\"%s\",\"width\":%d,\"height\":%d,\"sample_rate\":%d}%n",
                format, width, height, sampleRate);
        }
    }
}
