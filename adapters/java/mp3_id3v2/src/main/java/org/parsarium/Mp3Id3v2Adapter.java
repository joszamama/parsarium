package org.parsarium;

import java.nio.file.Path;

public final class Mp3Id3v2Adapter {
    private Mp3Id3v2Adapter() { }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) System.exit(2);
        Path path = Path.of(args[1]);
        if (args[0].equals("jaudiotagger")) {
            java.util.logging.Logger.getLogger("org.jaudiotagger")
                    .setLevel(java.util.logging.Level.OFF);
            var audio = org.jaudiotagger.audio.AudioFileIO.read(path.toFile());
            if (!(audio instanceof org.jaudiotagger.audio.mp3.MP3File)) System.exit(1);
            var mp3 = (org.jaudiotagger.audio.mp3.MP3File) audio;
            if (!mp3.hasID3v2Tag()) System.exit(1);
            var tag = mp3.getID3v2Tag();
            System.out.printf("{\"title\":\"%s\",\"artist\":\"%s\",\"album\":\"%s\"}%n",
                    tag.getFirst(org.jaudiotagger.tag.FieldKey.TITLE),
                    tag.getFirst(org.jaudiotagger.tag.FieldKey.ARTIST),
                    tag.getFirst(org.jaudiotagger.tag.FieldKey.ALBUM));
        } else if (args[0].equals("mp3agic")) {
            var mp3 = new com.mpatric.mp3agic.Mp3File(path);
            if (!mp3.hasId3v2Tag()) System.exit(1);
            var tag = mp3.getId3v2Tag();
            System.out.printf("{\"title\":\"%s\",\"artist\":\"%s\",\"album\":\"%s\",\"tag_version\":\"%s\"}%n",
                    tag.getTitle(), tag.getArtist(), tag.getAlbum(), tag.getVersion());
        } else if (args[0].equals("tika")) {
            var parser = new org.apache.tika.parser.mp3.Mp3Parser();
            var metadata = new org.apache.tika.metadata.Metadata();
            try (var stream = org.apache.tika.io.TikaInputStream.get(path)) {
                parser.parse(stream, new org.xml.sax.helpers.DefaultHandler(), metadata,
                        new org.apache.tika.parser.ParseContext());
            }
            System.out.printf("{\"title\":\"%s\",\"artist\":\"%s\",\"album\":\"%s\"}%n",
                    metadata.get("dc:title"), metadata.get("xmpDM:artist"),
                    metadata.get("xmpDM:album"));
        } else if (args[0].equals("jlayer")) {
            try (var input = java.nio.file.Files.newInputStream(path)) {
                var stream = new javazoom.jl.decoder.Bitstream(input);
                var header = stream.readFrame();
                if (header == null || stream.getRawID3v2() == null) System.exit(1);
                System.out.printf("{\"frequency\":%d,\"layer\":%d,\"id3v2_present\":true}%n",
                        header.frequency(), header.layer());
                stream.close();
            }
        } else if (args[0].equals("jave")) {
            var info = new ws.schild.jave.MultimediaObject(path.toFile()).getInfo();
            var audio = info.getAudio();
            System.out.printf("{\"format\":\"%s\",\"codec\":\"%s\",\"frequency\":%d,\"channels\":%d}%n",
                    info.getFormat(), audio.getDecoder(), audio.getSamplingRate(), audio.getChannels());
        } else if (args[0].equals("jaffree")) {
            var result = com.github.kokorin.jaffree.ffprobe.FFprobe
                    .atPath(Path.of(System.getenv().getOrDefault("PARSARIUM_FFPROBE_DIR", "/opt/homebrew/bin")))
                    .setShowStreams(true).setShowFormat(true).setInput(path).execute();
            var audio = result.getStreams().get(0);
            var format = result.getFormat();
            System.out.printf("{\"codec\":\"%s\",\"frequency\":%d,\"title\":\"%s\",\"artist\":\"%s\"}%n",
                    audio.getCodecName(), audio.getSampleRate(), format.getTag("title"), format.getTag("artist"));
        } else System.exit(2);
    }
}
