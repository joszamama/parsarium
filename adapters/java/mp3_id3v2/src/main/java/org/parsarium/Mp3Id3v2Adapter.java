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
        } else System.exit(2);
    }
}
