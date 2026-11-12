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
            case "jhove" -> {
                var module = new edu.harvard.hul.ois.jhove.module.WaveModule();
                module.setBase(new edu.harvard.hul.ois.jhove.JhoveBase());
                var info = new edu.harvard.hul.ois.jhove.RepInfo(file.toURI().toString());
                try (var stream = new java.io.FileInputStream(file)) {
                    module.parse(stream, info, 0);
                }
                var audio = module.getAESMetadata();
                System.out.printf("{\"format\":\"%s\",\"sample_rate\":%d,\"channels\":%d}%n",
                    info.getFormat(), (int) audio.getSampleRate(), audio.getNumChannels());
            }
            case "tarsos" -> {
                var dispatcher = be.tarsos.dsp.io.jvm.AudioDispatcherFactory.fromFile(file, 256, 0);
                var format = dispatcher.getFormat();
                final int[] frames = {0};
                dispatcher.addAudioProcessor(new be.tarsos.dsp.AudioProcessor() {
                    public boolean process(be.tarsos.dsp.AudioEvent event) {
                        frames[0] += event.getFloatBuffer().length;
                        return true;
                    }
                    public void processingFinished() { }
                });
                dispatcher.run();
                System.out.printf("{\"sample_rate\":%d,\"channels\":%d,\"bits\":%d,\"frames\":%d}%n",
                    (int) format.getSampleRate(), format.getChannels(), format.getSampleSizeInBits(), frames[0]);
            }
            case "musicg" -> {
                var wave = new com.musicg.wave.Wave(file.getAbsolutePath());
                var header = wave.getWaveHeader();
                System.out.printf("{\"format\":\"%s\",\"sample_rate\":%d,\"channels\":%d,\"bits\":%d,\"samples\":%d}%n",
                    header.getFormat(), header.getSampleRate(), header.getChannels(),
                    header.getBitsPerSample(), wave.getSampleAmplitudes().length);
            }
            default -> throw new IllegalArgumentException("unknown mode: " + mode);
        }
    }
}
