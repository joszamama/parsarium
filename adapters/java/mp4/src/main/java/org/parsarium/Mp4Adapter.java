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
            case "muxer" -> {
                var movie = org.mp4parser.muxer.container.mp4.MovieCreator.build(file.getAbsolutePath());
                var tracks = movie.getTracks();
                if (tracks.size() != 2) throw new IllegalStateException("expected two tracks in control");
                System.out.printf("{\"tracks\":%d,\"handlers\":[\"%s\",\"%s\"]}%n",
                    tracks.size(), tracks.get(0).getHandler(), tracks.get(1).getHandler());
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
            case "tika-mp4" -> {
                var parser = new org.apache.tika.parser.mp4.MP4Parser();
                var metadata = new org.apache.tika.metadata.Metadata();
                try (var stream = org.apache.tika.io.TikaInputStream.get(file.toPath())) {
                    parser.parse(stream, new org.xml.sax.helpers.DefaultHandler(), metadata,
                        new org.apache.tika.parser.ParseContext());
                }
                System.out.printf("{\"width\":%d,\"height\":%d,\"sample_rate\":%d,\"channels\":%d,\"title\":\"%s\"}%n",
                    Integer.parseInt(metadata.get("tiff:ImageWidth")),
                    Integer.parseInt(metadata.get("tiff:ImageLength")),
                    Integer.parseInt(metadata.get("xmpDM:audioSampleRate")),
                    Integer.parseInt(metadata.get("audio:channels")), metadata.get("dc:title"));
            }
            default -> throw new IllegalArgumentException("unknown mode: " + args[0]);
        }
    }
}
