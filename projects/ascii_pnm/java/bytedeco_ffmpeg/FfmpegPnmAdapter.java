package org.parsarium;

import java.io.File;

public final class FfmpegPnmAdapter {
    private FfmpegPnmAdapter() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 2) throw new IllegalArgumentException("usage: label local.ppm");
        File file = new File(args[1]);
        switch (args[0]) {
            case "javacv" -> {
                try (var grabber = new org.bytedeco.javacv.FFmpegFrameGrabber(file)) {
                    grabber.start();
                    var frame = grabber.grabImage();
                    if (frame == null) throw new IllegalStateException("No PNM frame decoded");
                    String codec = org.bytedeco.ffmpeg.global.avcodec.avcodec_get_name(grabber.getVideoCodec()).getString();
                    System.out.printf("{\"codec\":\"%s\",\"width\":%d,\"height\":%d,\"frame\":true}%n",
                        codec, grabber.getImageWidth(), grabber.getImageHeight());
                }
            }
            case "bytedeco-ffmpeg" -> {
                var context = org.bytedeco.ffmpeg.global.avformat.avformat_alloc_context();
                if (org.bytedeco.ffmpeg.global.avformat.avformat_open_input(
                        context, file.getAbsolutePath(), null, null) < 0)
                    throw new IllegalStateException("FFmpeg could not open PNM file");
                try {
                    if (org.bytedeco.ffmpeg.global.avformat.avformat_find_stream_info(context, (org.bytedeco.ffmpeg.avutil.AVDictionary)null) < 0)
                        throw new IllegalStateException("FFmpeg could not parse PNM stream");
                    var params = context.streams(0).codecpar();
                    String codec = org.bytedeco.ffmpeg.global.avcodec.avcodec_get_name(params.codec_id()).getString();
                    System.out.printf("{\"codec\":\"%s\",\"width\":%d,\"height\":%d}%n",
                        codec, params.width(), params.height());
                } finally {
                    org.bytedeco.ffmpeg.global.avformat.avformat_close_input(context);
                }
            }
            default -> throw new IllegalArgumentException("unknown adapter " + args[0]);
        }
    }
}
