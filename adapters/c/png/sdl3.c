#include <SDL3/SDL.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (!SDL_Init(0)) return 1;
    SDL_Surface *decoded = SDL_LoadPNG(argv[1]);
    if (!decoded) { fprintf(stderr, "SDL3: %s\n", SDL_GetError()); SDL_Quit(); return 1; }
    SDL_Surface *rgba = SDL_ConvertSurface(decoded, SDL_PIXELFORMAT_RGBA32);
    SDL_DestroySurface(decoded);
    if (!rgba) { SDL_Quit(); return 1; }
    if (rgba->w != 2 || rgba->h != 1 || rgba->pitch < 8) {
        SDL_DestroySurface(rgba); SDL_Quit(); return 1;
    }
    const unsigned char *pixels = rgba->pixels;
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           rgba->w, rgba->h, pixels[0], pixels[1], pixels[2], pixels[3],
           pixels[4], pixels[5], pixels[6], pixels[7]);
    SDL_DestroySurface(rgba);
    SDL_Quit();
    return 0;
}
