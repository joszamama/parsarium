package org.parsarium;

import java.io.File;
import org.bytedeco.javacv.FFmpegFrameGrabber;
import org.bytedeco.ffmpeg.avformat.AVFormatContext;
import static org.bytedeco.ffmpeg.global.avformat.*;

/** Local WAV input through the pinned JavaCV FFmpeg wrapper. */
public final class BytedecoWavAdapter {
    public static void main(String[] args) throws Exception {
        if (args.length != 2)
            throw new IllegalArgumentException("usage: BytedecoWavAdapter mode control.wav");
        switch (args[0]) {
            case "javacv" -> {
                try (var grabber = new FFmpegFrameGrabber(new File(args[1]))) {
                    grabber.start();
                    System.out.printf("{\"format\":\"%s\",\"codec\":\"%s\",\"sample_rate\":%d,\"channels\":%d}%n",
                        grabber.getFormat(), grabber.getAudioCodecName(),
                        grabber.getSampleRate(), grabber.getAudioChannels());
                }
            }
            case "ffmpeg" -> {
                AVFormatContext context = avformat_alloc_context();
                if (avformat_open_input(context, args[1], null, null) < 0)
                    throw new IllegalStateException("FFmpeg could not open WAV file");
                try {
                    if (avformat_find_stream_info(context, (org.bytedeco.ffmpeg.avutil.AVDictionary) null) < 0)
                        throw new IllegalStateException("FFmpeg could not read stream info");
                    var audio = context.streams(0).codecpar();
                    System.out.printf("{\"format\":\"%s\",\"sample_rate\":%d,\"channels\":%d}%n",
                        context.iformat().name().getString(), audio.sample_rate(), audio.ch_layout().nb_channels());
                } finally {
                    avformat_close_input(context);
                }
            }
            default -> throw new IllegalArgumentException("unknown mode: " + args[0]);
        }
    }
}
