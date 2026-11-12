package org.parsarium;

import java.io.File;

/** Parse the local MP4 with the Tallison MP4Parser distribution. */
public final class TallisonMp4Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: TallisonMp4Adapter control.mp4");
        try (var iso = new org.mp4parser.IsoFile(new File(args[0]))) {
            var movie = iso.getMovieBox();
            if (movie == null) throw new IllegalStateException("no moov box");
            System.out.printf("{\"tracks\":%d,\"timescale\":%d}%n",
                movie.getTrackCount(), movie.getMovieHeaderBox().getTimescale());
        }
    }
}
