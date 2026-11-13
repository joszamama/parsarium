#include <eminem/from_text.hpp>
#include <cstdio>

int main(int argc, char **argv) {
  if (argc != 2) return 2;
  auto parser = eminem::parse_text_file(argv[1], {});
  parser.scan_preamble();
  if (parser.get_banner().field != eminem::Field::REAL) return 1;
  std::size_t count = 0;
  double entry = 0;
  parser.scan_real([&](std::size_t row, std::size_t col, double value) {
    ++count;
    if (row == 1 && col == 3) entry = value;
  });
  std::printf("{\"rows\":%zu,\"cols\":%zu,\"nnz\":%zu,\"entry_1_3\":%.1f}\n",
              static_cast<std::size_t>(parser.get_nrows()),
              static_cast<std::size_t>(parser.get_ncols()), count, entry);
  return 0;
}
