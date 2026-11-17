package org.parsarium;

import java.nio.ByteBuffer;
import org.jaudiotagger.audio.exceptions.InvalidAudioFrameException;
import org.jaudiotagger.audio.mp3.MPEGFrameHeader;

/** Parse the first MPEG Layer III frame header of an untagged local byte stream. */
public final class Mp3Adapter {
    private Mp3Adapter() { }

    public static String parse(byte[] data) throws InvalidAudioFrameException {
        if (data.length < MPEGFrameHeader.HEADER_SIZE || data.length > (1 << 20))
            throw new IllegalArgumentException("input outside harness limit");
        ByteBuffer bytes = ByteBuffer.wrap(data);
        if (!MPEGFrameHeader.isMPEGFrame(bytes))
            throw new InvalidAudioFrameException("no MPEG frame at byte zero");
        MPEGFrameHeader header = MPEGFrameHeader.parseMPEGHeader(bytes);
        if (header.getLayer() != MPEGFrameHeader.LAYER_III ||
            header.getSamplingRate() == null || header.getBitRate() == null)
            throw new InvalidAudioFrameException("not a complete Layer III header");
        return String.format("{\"codec\":\"MP3\",\"mpeg_version\":\"%s\",\"layer\":\"%s\",\"sample_rate\":%d,\"channels\":%d,\"bitrate_kbps\":%d}",
                header.getVersionAsString(), header.getLayerAsString(),
                header.getSamplingRate(), header.getNumberOfChannels(), header.getBitRate());
    }
}
