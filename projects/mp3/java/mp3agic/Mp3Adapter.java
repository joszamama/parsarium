package org.parsarium;

import com.mpatric.mp3agic.InvalidDataException;
import com.mpatric.mp3agic.Mp3File;
import com.mpatric.mp3agic.UnsupportedTagException;
import java.io.IOException;
import java.nio.file.Path;

/** Report only verified Layer III header fields from mp3agic's local-file scanner. */
public final class Mp3Adapter {
    private Mp3Adapter() { }

    public static String parse(Path input) throws IOException, UnsupportedTagException, InvalidDataException {
        Mp3File mp3 = new Mp3File(input);
        if (!"III".equals(mp3.getLayer()))
            throw new InvalidDataException("not MPEG Layer III");
        return String.format("{\"codec\":\"MP3\",\"mpeg_version\":\"%s\",\"layer\":\"%s\",\"sample_rate\":%d,\"channel_mode\":\"%s\",\"bitrate_kbps\":%d}",
                mp3.getVersion(), mp3.getLayer(), mp3.getSampleRate(),
                mp3.getChannelMode(), mp3.getBitrate());
    }
}
