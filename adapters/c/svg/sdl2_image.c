#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    if (SDL_Init(0) != 0) return 1;
    SDL_RWops *stream = SDL_RWFromFile(argv[1], "rb");
    if (!stream) { SDL_Quit(); return 1; }
    SDL_Surface *decoded = IMG_LoadSVG_RW(stream);
    SDL_RWclose(stream);
    if (!decoded) { fprintf(stderr, "SDL2_image: %s\n", IMG_GetError()); SDL_Quit(); return 1; }
    SDL_Surface *rgba = SDL_ConvertSurfaceFormat(decoded, SDL_PIXELFORMAT_RGBA32, 0);
    SDL_FreeSurface(decoded);
    if (!rgba) { SDL_Quit(); return 1; }
    if (rgba->w != 2 || rgba->h != 1 || rgba->pitch < 8) {
        SDL_FreeSurface(rgba); SDL_Quit(); return 1;
    }
    const unsigned char *pixels = (const unsigned char *)rgba->pixels;
    printf("{\"width\":%d,\"height\":%d,\"first\":[%u,%u,%u,%u],\"second\":[%u,%u,%u,%u]}\n",
           rgba->w, rgba->h, pixels[0], pixels[1], pixels[2], pixels[3],
           pixels[4], pixels[5], pixels[6], pixels[7]);
    SDL_FreeSurface(rgba);
    SDL_Quit();
    return 0;
}
