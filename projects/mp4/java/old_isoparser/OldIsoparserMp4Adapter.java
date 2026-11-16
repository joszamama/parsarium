package org.parsarium;

/** Parse the local MP4 with the older CoreMedia MP4Parser distribution. */
public final class OldIsoparserMp4Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: OldIsoparserMp4Adapter control.mp4");
        try (var iso = new com.coremedia.iso.IsoFile(args[0])) {
            var movie = iso.getMovieBox();
            if (movie == null) throw new IllegalStateException("no moov box");
            System.out.printf("{\"tracks\":%d,\"timescale\":%d}%n",
                movie.getTrackCount(), movie.getMovieHeaderBox().getTimescale());
        }
    }
}
