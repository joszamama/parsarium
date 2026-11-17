package org.parsarium;

import java.io.File;
import java.nio.ByteBuffer;

public final class Mp3Adapter {
    private Mp3Adapter() { }

    // Demuxes every MPEG audio frame from a local file with MPEGAudioDemuxer
    // and decodes each one with Mp3Decoder. The stream format comes from the
    // decoder's own header parse of the first frame; decoded_samples counts
    // 16-bit PCM samples per channel over all decoded frames.
    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("jcodec")) System.exit(2);
        org.jcodec.common.logging.Logger.setLevel(org.jcodec.common.logging.LogLevel.ERROR);
        var decoder = new org.jcodec.codecs.mpa.Mp3Decoder();
        int sampleRate = 0, channels = 0, frames = 0;
        long decodedBytes = 0;
        String codec;
        try (var channel = org.jcodec.common.io.NIOUtils.readableChannel(new File(args[1]));
             var demuxer = new org.jcodec.containers.mp3.MPEGAudioDemuxer(channel)) {
            var track = demuxer.getAudioTracks().get(0);
            if (track.getMeta() == null) System.exit(1);
            codec = track.getMeta().getCodec().toString();
            for (var packet = track.nextFrame(); packet != null; packet = track.nextFrame()) {
                ByteBuffer data = packet.getData();
                if (frames == 0) {
                    var format = decoder.getCodecMeta(data).getFormat();
                    sampleRate = format.getSampleRate();
                    channels = format.getChannels();
                }
                var pcm = decoder.decodeFrame(data, ByteBuffer.allocate(1152 * 2 * 2));
                decodedBytes += pcm.getData().remaining();
                frames++;
            }
        }
        if (frames == 0) System.exit(1);
        System.out.printf("{\"codec\":\"%s\",\"sample_rate\":%d,\"channels\":%d,\"frames\":%d,\"decoded_samples\":%d}%n",
                codec, sampleRate, channels, frames, decodedBytes / (2L * channels));
    }
}
