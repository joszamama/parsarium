#include <mlt++/Mlt.h>
#include <cstdio>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!Mlt::Factory::init()) return 1;
    {
        Mlt::Profile profile;
        Mlt::Producer producer(profile, "avformat", argv[1]);
        if (!producer.is_valid()) return 1;
        const char *video = producer.get("meta.media.0.codec.name");
        const char *audio = producer.get("meta.media.1.codec.name");
        if (!video || !audio) return 1;
        std::printf("{\"streams\":%d,\"video_codec\":\"%s\",\"audio_codec\":\"%s\",\"width\":%d,\"height\":%d}\n",
                    producer.get_int("meta.media.nb_streams"), video, audio,
                    producer.get_int("meta.media.0.codec.width"),
                    producer.get_int("meta.media.0.codec.height"));
    }
    Mlt::Factory::close();
    return 0;
}
