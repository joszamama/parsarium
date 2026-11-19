"""Run one documented local MP4 reader and print observable parsed fields."""

import json
import sys


def red(pixel):
    return bool(pixel[0] > 240 and pixel[1] < 20 and pixel[2] < 20)


def parse(name, path):
    if name == "mutagen":
        from mutagen.mp4 import MP4
        doc = MP4(path)
        return {"title": doc.tags["©nam"][0]}
    if name == "tinytag":
        from tinytag import TinyTag
        doc = TinyTag.get(path)
        return {"title": doc.title, "duration_seconds": round(doc.duration, 3)}
    if name == "pytaglib":
        import taglib
        with taglib.File(path) as doc:
            return {"title": doc.tags["TITLE"][0]}
    if name == "pymediainfo":
        from pymediainfo import MediaInfo
        tracks = MediaInfo.parse(path).tracks
        video = next(track for track in tracks if track.track_type == "Video")
        audio = next(track for track in tracks if track.track_type == "Audio")
        return {"width": int(video.width), "height": int(video.height),
                "video_format": video.format, "audio_format": audio.format}
    if name == "hachoir":
        from hachoir.parser import createParser
        from hachoir.metadata import extractMetadata
        doc = createParser(path)
        try:
            metadata = extractMetadata(doc)
            return {"width": metadata.get("width"), "height": metadata.get("height"),
                    "duration_seconds": int(metadata.get("duration").total_seconds())}
        finally:
            doc.stream.close()
    if name == "pydub":
        from pydub import AudioSegment
        doc = AudioSegment.from_file(path)
        return {"audio_rate": doc.frame_rate, "audio_channels": doc.channels,
                "duration_ms": len(doc)}
    if name == "audioread":
        import audioread
        with audioread.audio_open(path) as doc:
            return {"audio_rate": doc.samplerate, "audio_channels": doc.channels,
                    "duration_seconds": round(doc.duration, 3)}
    if name == "av":
        import av
        with av.open(path) as doc:
            result = {}
            if "title" in doc.metadata:
                result["title"] = doc.metadata["title"]
            if doc.streams.video:
                video = doc.streams.video[0]
                result.update(width=video.codec_context.width,
                              height=video.codec_context.height,
                              video_codec=video.codec_context.name)
            if doc.streams.audio:
                result["audio_codec"] = doc.streams.audio[0].codec_context.name
            return result
    if name == "audiomath":
        import audiomath
        doc = audiomath.Sound(path)
        return {"audio_rate": int(doc.fs), "audio_samples": doc.nSamples}
    if name == "ffmpeg-python":
        import ffmpeg
        doc = ffmpeg.probe(path)
        result = {}
        tags = doc["format"].get("tags", {})
        if "title" in tags:
            result["title"] = tags["title"]
        video = next((stream for stream in doc["streams"]
                      if stream["codec_type"] == "video"), None)
        if video is not None:
            result.update(width=video["width"], height=video["height"],
                          video_codec=video["codec_name"])
        return result
    if name == "moviepy":
        from moviepy import VideoFileClip
        with VideoFileClip(path) as doc:
            frame = doc.get_frame(0)
            return {"width": doc.size[0], "height": doc.size[1],
                    "duration_seconds": round(doc.duration, 3),
                    "red_frame": red(frame[0, 0])}
    if name == "imageio":
        import imageio.v2 as imageio
        doc = imageio.get_reader(path)
        try:
            frame = doc.get_data(0)
            return {"width": frame.shape[1], "height": frame.shape[0],
                    "video_codec": doc.get_meta_data()["codec"],
                    "red_frame": red(frame[0, 0])}
        finally:
            doc.close()
    if name == "imageio-ffmpeg":
        import imageio_ffmpeg
        frames = imageio_ffmpeg.read_frames(path)
        try:
            header = next(frames)
            frame = next(frames)
            return {"width": header["size"][0], "height": header["size"][1],
                    "video_codec": header["codec"],
                    "red_frame": red(frame[:3])}
        finally:
            frames.close()
    if name == "opencv-python-headless":
        import cv2
        doc = cv2.VideoCapture(path)
        try:
            ok, frame = doc.read()
            if not ok:
                raise RuntimeError("OpenCV did not decode a video frame")
            return {"width": frame.shape[1], "height": frame.shape[0],
                    "red_frame": bool(frame[0, 0, 2] > 240 and
                                      frame[0, 0, 1] < 20 and frame[0, 0, 0] < 20)}
        finally:
            doc.release()
    if name == "pymp4":
        from pymp4.parser import Box
        with open(path, "rb") as stream:
            first = Box.parse_stream(stream)
            second = Box.parse_stream(stream)
            return {"first_box": first.type.decode(), "major_brand": first.major_brand.decode(),
                    "second_box": second.type.decode()}
    if name == "metabeam":
        import metabeam
        doc = metabeam.parse(path)["mp4"]
        return {"major_brand": doc["major_brand"], "timescale": doc["timescale"],
                "boxes": [box["type"] for box in doc["top_level_boxes"]]}
    if name == "ffmpegio":
        import ffmpegio
        doc = ffmpegio.probe.full_details(path)
        video = next(stream for stream in doc["streams"] if stream["codec_type"] == "video")
        return {"title": doc["format"]["tags"]["title"], "width": video["width"],
                "height": video["height"], "video_codec": video["codec_name"]}
    if name == "pymp4v2":
        import pymp4v2
        with pymp4v2.MP4File(path, mode="r") as doc:
            return {"title": doc.tags.name, "tracks": len(doc.tracks),
                    "duration_seconds": round(doc.duration / doc.timescale, 3)}
    if name == "pycord":
        from pycord.video_reader import VideoReader
        doc = VideoReader(path)
        frames = doc.get_range(0, 1)
        return {"frames": len(doc), "width": frames.shape[2], "height": frames.shape[1],
                "red_frame": red(frames[0, 0, 0])}
    if name == "pyvideoreader":
        from videoreader import VideoReader
        doc = VideoReader(path)
        try:
            return {"frames": doc.number_of_frames, "width": doc.frame_width,
                    "height": doc.frame_height, "channels": doc.frame_channels}
        finally:
            doc.close()
    raise ValueError(f"unknown MP4 adapter: {name}")


if __name__ == "__main__":
    print(json.dumps(parse(sys.argv[1], sys.argv[2]), sort_keys=True))
