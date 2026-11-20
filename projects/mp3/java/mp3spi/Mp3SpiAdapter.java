package org.parsarium;

import java.nio.file.Path;

/** Read the local tagged MP3 with the pinned MP3SPI provider, independent of Java Sound discovery. */
public final class Mp3SpiAdapter {
    private Mp3SpiAdapter() { }

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

    static String text(Object value) {
        return value == null ? null : String.valueOf(value);
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
        if (args.length != 1) System.exit(2);
        var reader = new javazoom.spi.mpeg.sampled.file.MpegAudioFileReader();
        var format = reader.getAudioFileFormat(Path.of(args[0]).toFile());
        var props = format.properties();
        System.out.println(object("type", text(format.getType()), "title", text(props.get("title")),
                "artist", text(props.get("author")), "album", text(props.get("album")),
                "tag_version", text(props.get("mp3.id3tag.v2.version"))));
    }
}
