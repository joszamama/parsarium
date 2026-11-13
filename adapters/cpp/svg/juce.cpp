#include <juce_graphics/juce_graphics.h>
#include <cstdio>

int main(int argc, char** argv) {
  if (argc != 2) return 2;
  auto drawable = juce::Drawable::createFromSVGFile(juce::File(argv[1]));
  if (!drawable) return 1;
  const auto bounds = drawable->getDrawableBounds();
  std::printf("{\"width\":%.0f,\"height\":%.0f}\n",
              bounds.getWidth(), bounds.getHeight());
  return 0;
}
