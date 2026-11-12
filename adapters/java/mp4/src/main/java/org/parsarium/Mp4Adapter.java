package org.parsarium;

import java.io.File;

/** Each mode parses the supplied local MP4 through a separate public API. */
public final class Mp4Adapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("usage: Mp4Adapter mode control.mp4");
        File file = new File(args[1]);
        switch (args[0]) {
            case "isoparser" -> {
                try (var iso = new org.mp4parser.IsoFile(file)) {
                    var movie = iso.getMovieBox();
                    if (movie == null) throw new IllegalStateException("no moov box");
                    System.out.printf("{\"tracks\":%d,\"timescale\":%d}%n",
                        movie.getTrackCount(), movie.getMovieHeaderBox().getTimescale());
                }
            }
            case "metadata-extractor" -> {
                var metadata = com.drew.imaging.mp4.Mp4MetadataReader.readMetadata(file);
                var video = metadata.getFirstDirectoryOfType(com.drew.metadata.mp4.media.Mp4VideoDirectory.class);
                if (video == null) throw new IllegalStateException("no MP4 video directory");
                System.out.printf("{\"width\":%d,\"height\":%d}%n",
                    video.getInt(com.drew.metadata.mp4.media.Mp4VideoDirectory.TAG_WIDTH),
                    video.getInt(com.drew.metadata.mp4.media.Mp4VideoDirectory.TAG_HEIGHT));
            }
            case "jcodec" -> {
                var movie = org.jcodec.containers.mp4.MP4Util.parseMovie(file);
                var video = movie.getVideoTrack();
                if (video == null) throw new IllegalStateException("no MP4 video track");
                System.out.printf("{\"tracks\":%d,\"video_width\":%d,\"video_height\":%d}%n",
                    movie.getTracks().length, video.getCodedSize().getWidth(), video.getCodedSize().getHeight());
            }
            default -> throw new IllegalArgumentException("unknown mode: " + args[0]);
        }
    }
}
