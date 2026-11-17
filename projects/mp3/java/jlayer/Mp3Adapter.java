package org.parsarium;

import java.io.FileInputStream;
import javazoom.jl.decoder.Bitstream;
import javazoom.jl.decoder.Decoder;
import javazoom.jl.decoder.Header;
import javazoom.jl.decoder.SampleBuffer;

/** Read and decode every Layer III frame in a local untagged stream. */
public final class Mp3Adapter {
    private Mp3Adapter() { }

    public static void main(String[] args) throws Exception {
        if (args.length != 2 || !args[0].equals("jlayer")) throw new IllegalArgumentException("jlayer input.mp3");
        int sampleRate = 0, channels = 0, frames = 0;
        long samples = 0;
        try (FileInputStream input = new FileInputStream(args[1])) {
            Bitstream stream = new Bitstream(input);
            Decoder decoder = new Decoder();
            try {
                for (Header header = stream.readFrame(); header != null; header = stream.readFrame()) {
                    try {
                        if (header.layer() != 3) throw new IllegalArgumentException("not Layer III");
                        SampleBuffer pcm = (SampleBuffer) decoder.decodeFrame(header, stream);
                        if (frames == 0) {
                            sampleRate = decoder.getOutputFrequency();
                            channels = decoder.getOutputChannels();
                        }
                        if (decoder.getOutputFrequency() != sampleRate ||
                            decoder.getOutputChannels() != channels) {
                            throw new IllegalArgumentException("changing stream format");
                        }
                        samples += pcm.getBufferLength() / channels;
                        frames++;
                    } finally {
                        stream.closeFrame();
                    }
                }
            } finally {
                stream.close();
            }
        }
        if (frames == 0) throw new IllegalArgumentException("no frames");
        System.out.printf("{\"codec\":\"MP3\",\"sample_rate\":%d,\"channels\":%d,\"frames\":%d,\"decoded_samples\":%d}%n",
                sampleRate, channels, frames, samples);
    }
}
