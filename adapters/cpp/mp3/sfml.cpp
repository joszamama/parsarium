#include <SFML/Audio/InputSoundFile.hpp>
#include <cstdint>
#include <iostream>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  sf::InputSoundFile file;
  if (!file.openFromFile(argv[1])) return 1;
  std::int16_t sample = 0;
  std::uint64_t decoded = file.read(&sample, 1);
  if (decoded != 1) return 1;
  std::cout << "{\"samples\":" << file.getSampleCount()
            << ",\"sample_rate\":" << file.getSampleRate()
            << ",\"channels\":" << file.getChannelCount()
            << ",\"decoded_samples\":" << decoded << "}\n";
  return 0;
}
