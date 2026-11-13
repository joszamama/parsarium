#include <framework/mlt.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!mlt_factory_init(NULL)) return 1;
    mlt_profile profile = mlt_profile_init(NULL);
    if (!profile) { mlt_factory_close(); return 1; }
    mlt_producer producer = mlt_factory_producer(profile, "avformat", argv[1]);
    if (!producer) { mlt_profile_close(profile); mlt_factory_close(); return 1; }
    mlt_properties properties = mlt_producer_properties(producer);
    const char *video = mlt_properties_get(properties, "meta.media.0.codec.name");
    const char *audio = mlt_properties_get(properties, "meta.media.1.codec.name");
    if (!video || !audio) return 1;
    printf("{\"streams\":%d,\"video_codec\":\"%s\",\"audio_codec\":\"%s\",\"width\":%d,\"height\":%d}\n",
           mlt_properties_get_int(properties, "meta.media.nb_streams"), video, audio,
           mlt_properties_get_int(properties, "meta.media.0.codec.width"),
           mlt_properties_get_int(properties, "meta.media.0.codec.height"));
    mlt_producer_close(producer);
    mlt_profile_close(profile);
    mlt_factory_close();
    return 0;
}
