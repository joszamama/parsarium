#include <SDL3_mixer/SDL_mixer.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!MIX_Init()) return 3;
    MIX_Audio *audio = MIX_LoadAudio(NULL, argv[1], true);
    if (!audio) return 4;
    SDL_AudioSpec spec;
    Sint64 frames = MIX_GetAudioDuration(audio);
    if (!MIX_GetAudioFormat(audio, &spec) || frames < 0) return 5;
    printf("{\"sample_rate\":%d,\"channels\":%d,\"frames\":%lld}\n",
           spec.freq, spec.channels, (long long)frames);
    MIX_DestroyAudio(audio);
    MIX_Quit();
    return 0;
}
