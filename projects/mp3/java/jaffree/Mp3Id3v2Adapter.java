package org.parsarium;

import java.nio.file.Path;

public final class Mp3Id3v2Adapter {
    private Mp3Id3v2Adapter() { }

    /** JSON string literal; non-ASCII characters are written as \\uXXXX escapes. */
    static String quote(String value) {
        StringBuilder out = new StringBuilder("\"");
        for (char c : value.toCharArray()) {
            if (c == '"' || c == '\\') out.append('\\').append(c);
            else if (c < 0x20 || c > 0x7e) out.append(String.format("\\u%04x", (int) c));
            else out.append(c);
        }
        return out.append('"').toString();
    }

    /** JSON object of the non-null values, in the given key order. */
    static String object(Object... pairs) {
        StringBuilder out = new StringBuilder("{");
        for (int i = 0; i < pairs.length; i += 2) {
            if (pairs[i + 1] == null) continue;
            if (out.length() > 1) out.append(',');
            Object value = pairs[i + 1];
            out.append(quote((String) pairs[i])).append(':')
               .append(value instanceof String text ? quote(text) : String.valueOf(value));
        }
        return out.append('}').toString();
    }

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
            var tag = mp3.hasId3v2Tag() ? mp3.getId3v2Tag() : null;
            System.out.println(tag == null ? "{}" : object("title", tag.getTitle(), "artist", tag.getArtist(),
                    "album", tag.getAlbum(), "tag_version", tag.getVersion()));
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
                if (header == null) System.exit(1);
                System.out.printf("{\"frequency\":%d,\"layer\":%d,\"id3v2_present\":%s}%n",
                        header.frequency(), header.layer(), stream.getRawID3v2() != null);
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
            System.out.println(object("codec", audio.getCodecName(), "frequency", audio.getSampleRate(),
                    "title", format.getTag("title"), "artist", format.getTag("artist")));
        } else if (args[0].equals("jcodec")) {
            org.jcodec.common.logging.Logger.setLevel(org.jcodec.common.logging.LogLevel.ERROR);
            try (var channel = org.jcodec.common.io.NIOUtils.readableChannel(path.toFile());
                 var demuxer = new org.jcodec.containers.mp3.MPEGAudioDemuxer(channel)) {
                var track = demuxer.getAudioTracks().get(0);
                var frame = track.nextFrame();
                if (frame == null) System.exit(1);
                System.out.printf("{\"codec\":\"%s\",\"frame_bytes\":%d,\"timescale\":%d}%n",
                        track.getMeta().getCodec(), frame.getData().remaining(), frame.getTimescale());
            }
        } else if (args[0].equals("codecmedia")) {
            var result = me.tamkungz.codecmedia.CodecMedia.createDefault().probe(path);
            var audio = result.streams().get(0);
            System.out.printf("{\"codec\":\"%s\",\"frequency\":%d,\"channels\":%d}%n",
                    audio.codec(), audio.sampleRate(), audio.channels());
        } else if (args[0].equals("jid3lib")) {
            var mp3 = new org.farng.mp3.MP3File(path.toFile());
            if (!mp3.hasID3v2Tag()) System.exit(1);
            var tag = mp3.getID3v2Tag();
            System.out.printf("{\"title\":\"%s\",\"artist\":\"%s\",\"album\":\"%s\"}%n",
                    tag.getSongTitle(), tag.getLeadArtist(), tag.getAlbumTitle());
        } else if (args[0].equals("taglib")) {
            try (var mp3 = new cz.skyba.taglib.mpeg.MpegFile(path)) {
                if (!mp3.hasId3v2Tag()) System.exit(1);
                var tag = mp3.id3v2Tag();
                var props = mp3.detailedProperties();
                System.out.printf("{\"title\":\"%s\",\"artist\":\"%s\",\"album\":\"%s\",\"frequency\":%d}%n",
                        tag.title(), tag.artist(), tag.album(), props.sampleRate());
            }
        } else if (args[0].equals("javamp3")) {
            try (var input = new java.io.BufferedInputStream(java.nio.file.Files.newInputStream(path));
                 var sound = new fr.delthas.javamp3.Sound(input)) {
                byte[] samples = new byte[32];
                int bytes = sound.read(samples);
                System.out.printf("{\"frequency\":%d,\"stereo\":%s,\"sample_bytes\":%d}%n",
                        sound.getSamplingFrequency(), sound.isStereo(), bytes);
            }
        } else System.exit(2);
    }
}
