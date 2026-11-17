package org.parsarium;

import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.UnsupportedAudioFileException;
import javazoom.spi.mpeg.sampled.file.MpegAudioFileReader;
import javazoom.spi.mpeg.sampled.convert.MpegFormatConversionProvider;

/** Parse an untagged MPEG Layer III stream through MP3SPI and decode all PCM samples. */
public final class Mp3SpiAdapter {
    private Mp3SpiAdapter() { }

    public static String parse(byte[] data) throws IOException, UnsupportedAudioFileException {
        MpegAudioFileReader reader = new MpegAudioFileReader();
        try (BufferedInputStream input = new BufferedInputStream(new ByteArrayInputStream(data));
             AudioInputStream encoded = reader.getAudioInputStream(input)) {
            AudioFormat source = encoded.getFormat();
            String encoding = source.getEncoding().toString();
            if (!encoding.equals("MPEG1L3") && !encoding.equals("MPEG2L3") &&
                !encoding.equals("MPEG2DOT5L3")) {
                throw new UnsupportedAudioFileException("not MPEG Layer III");
            }
            int sampleRate = Math.round(source.getSampleRate());
            int channels = source.getChannels();
            if (sampleRate <= 0 || channels < 1 || channels > 2)
                throw new UnsupportedAudioFileException("invalid Layer III format");
            AudioFormat pcmFormat = new AudioFormat(AudioFormat.Encoding.PCM_SIGNED,
                    sampleRate, 16, channels, 2 * channels, sampleRate, false);
            MpegFormatConversionProvider provider = new MpegFormatConversionProvider();
            long pcmBytes = 0;
            try (AudioInputStream pcm = provider.getAudioInputStream(pcmFormat, encoded)) {
                byte[] buffer = new byte[8192];
                for (int size; (size = pcm.read(buffer)) != -1; ) {
                    pcmBytes += size;
                    if (pcmBytes > (64L << 20)) throw new IOException("decoded stream too large");
                }
            }
            if (pcmBytes == 0 || pcmBytes % (2L * channels) != 0)
                throw new UnsupportedAudioFileException("incomplete PCM decode");
            long samples = pcmBytes / (2L * channels);
            int samplesPerFrame = encoding.equals("MPEG1L3") ? 1152 : 576;
            if (samples % samplesPerFrame != 0)
                throw new UnsupportedAudioFileException("partial Layer III frame");
            long frames = samples / samplesPerFrame;
            return String.format("{\"codec\":\"MP3\",\"sample_rate\":%d,\"channels\":%d,\"frames\":%d,\"decoded_samples\":%d}",
                    sampleRate, channels, frames, samples);
        }
    }
}
