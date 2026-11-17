package org.parsarium;

import java.nio.file.Path;

/** Read the local tagged MP3 with the pinned MP3SPI provider, independent of Java Sound discovery. */
public final class Mp3SpiAdapter {
    private Mp3SpiAdapter() { }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) System.exit(2);
        var reader = new javazoom.spi.mpeg.sampled.file.MpegAudioFileReader();
        var format = reader.getAudioFileFormat(Path.of(args[0]).toFile());
        var props = format.properties();
        System.out.printf("{\"type\":\"%s\",\"title\":\"%s\",\"artist\":\"%s\",\"album\":\"%s\",\"tag_version\":\"%s\"}%n",
                format.getType(), props.get("title"), props.get("author"), props.get("album"),
                props.get("mp3.id3tag.v2.version"));
    }
}
