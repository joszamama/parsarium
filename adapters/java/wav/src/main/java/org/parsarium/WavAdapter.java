package org.parsarium;

import java.io.File;
import java.nio.file.Path;

/** One documented local-input path per mode; output comes from the supplied WAV file. */
public final class WavAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("usage: WavAdapter mode control.wav");
        String mode = args[0];
        File file = new File(args[1]);
        switch (mode) {
            case "wavfile" -> {
                var reader = com.github.psambit9791.wavfile.WavFile.openWavFile(file);
                try {
                    int[] samples = new int[4];
                    if (reader.readFrames(samples, 4) != 4) throw new IllegalStateException("four samples required");
                    System.out.printf("{\"sample_rate\":%d,\"channels\":%d,\"frames\":%d,\"samples\":[%d,%d,%d,%d]}%n",
                        reader.getSampleRate(), reader.getNumChannels(), reader.getNumFrames(),
                        samples[0], samples[1], samples[2], samples[3]);
                } finally { reader.close(); }
            }
            case "jaudiotagger" -> {
                var header = org.jaudiotagger.audio.AudioFileIO.read(file).getAudioHeader();
                System.out.printf("{\"sample_rate\":%d,\"channels\":\"%s\",\"bits\":%d}%n",
                    header.getSampleRateAsNumber(), header.getChannels(), header.getBitsPerSample());
            }
            case "jcodec" -> {
                try (var reader = new org.jcodec.codecs.wav.WavInput.WavFile(file)) {
                    var format = reader.getFormat();
                    System.out.printf("{\"sample_rate\":%d,\"channels\":%d,\"bits\":%d}%n",
                        format.getSampleRate(), format.getChannels(), format.getSampleSizeInBits());
                }
            }
            case "beads" -> {
                var reader = new net.beadsproject.beads.data.audiofile.WavFileReaderWriter();
                float[][] samples = reader.readAudioFile(file.getAbsolutePath());
                var format = reader.getSampleAudioFormat();
                System.out.printf("{\"sample_rate\":%d,\"channels\":%d,\"frames\":%d}%n",
                    (int) format.sampleRate, format.channels, samples[0].length);
            }
            case "codecmedia" -> {
                var result = me.tamkungz.codecmedia.CodecMedia.createDefault().probe(Path.of(args[1]));
                var audio = result.streams().get(0);
                System.out.printf("{\"codec\":\"%s\",\"sample_rate\":%d,\"channels\":%d}%n",
                    audio.codec(), audio.sampleRate(), audio.channels());
            }
            case "jdsp" -> {
                var reader = new com.github.psambit9791.jdsp.io.WAV();
                reader.readWAV(file.getAbsolutePath());
                var props = reader.getProperties();
                System.out.printf("{\"sample_rate\":%d,\"channels\":%d,\"frames\":%d}%n",
                    props.get("SampleRate"), props.get("Channels"), props.get("Frames"));
            }
            case "tika" -> {
                var parser = new org.apache.tika.parser.audio.AudioParser();
                var metadata = new org.apache.tika.metadata.Metadata();
                try (var stream = org.apache.tika.io.TikaInputStream.get(file.toPath())) {
                    parser.parse(stream, new org.xml.sax.helpers.DefaultHandler(), metadata,
                        new org.apache.tika.parser.ParseContext());
                }
                System.out.printf("{\"sample_rate\":%d,\"channels\":%d}%n",
                    Integer.parseInt(metadata.get("xmpDM:audioSampleRate")),
                    Integer.parseInt(metadata.get("audio:channels")));
            }
            default -> throw new IllegalArgumentException("unknown mode: " + mode);
        }
    }
}
