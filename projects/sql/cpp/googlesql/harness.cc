// GoogleSQL parser harness: reads one local SQL file, parses every statement with
// googlesql::ParseNextStatement (default LanguageOptions, no catalog, no analyzer) and walks
// the returned AST to print the oracle summary as one JSON line.
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <memory>
#include <set>
#include <string>
#include <utility>
#include <vector>

#include "absl/status/status.h"
#include "absl/strings/ascii.h"
#include "googlesql/parser/parse_tree.h"
#include "googlesql/parser/parser.h"
#include "googlesql/public/language_options.h"
#include "googlesql/public/parse_resume_location.h"

namespace {

using namespace googlesql;  // NOLINT

struct Summary {
  std::string kind;
  std::set<std::string> tables;
  std::set<std::string> functions;
  std::set<std::pair<std::string, std::string>> literals;
  int select_items = 0, joins = 0, group_by = 0, order_by = 0, columns = 0, rows = 0;
  bool where = false;
};

std::string Lower(std::string text) { return absl::AsciiStrToLower(text); }

void Walk(const ASTNode *node, Summary *out) {
  if (node == nullptr) return;
  if (auto *select = node->GetAsOrNull<ASTSelect>()) {
    out->select_items += static_cast<int>(select->select_list()->columns().size());
    if (select->where_clause() != nullptr) out->where = true;
    if (select->group_by() != nullptr) {
      out->group_by += static_cast<int>(select->group_by()->grouping_items().size());
    }
  } else if (auto *order = node->GetAsOrNull<ASTOrderBy>()) {
    out->order_by += static_cast<int>(order->ordering_expressions().size());
  } else if (node->GetAsOrNull<ASTJoin>() != nullptr) {
    out->joins += 1;
  } else if (auto *table = node->GetAsOrNull<ASTTablePathExpression>()) {
    if (table->path_expr() != nullptr) {
      out->tables.insert(Lower(table->path_expr()->ToIdentifierPathString()));
    }
  } else if (auto *call = node->GetAsOrNull<ASTFunctionCall>()) {
    out->functions.insert(Lower(call->function()->ToIdentifierPathString()));
  } else if (auto *insert = node->GetAsOrNull<ASTInsertStatement>()) {
    if (auto *target = insert->target_path()->GetAsOrNull<ASTPathExpression>()) {
      out->tables.insert(Lower(target->ToIdentifierPathString()));
    }
    if (insert->column_list() != nullptr) {
      out->columns = static_cast<int>(insert->column_list()->column_items().size());
    }
    if (insert->rows() != nullptr) {
      out->rows = static_cast<int>(insert->rows()->rows().size());
    }
  } else if (auto *text = node->GetAsOrNull<ASTStringLiteral>()) {
    out->literals.insert({"string", text->string_value()});
  } else if (auto *integer = node->GetAsOrNull<ASTIntLiteral>()) {
    out->literals.insert({"number", std::string(integer->image())});
  } else if (auto *decimal = node->GetAsOrNull<ASTFloatLiteral>()) {
    out->literals.insert({"number", std::string(decimal->image())});
  }
  for (int i = 0; i < node->num_children(); ++i) Walk(node->child(i), out);
}

std::string Quote(const std::string &text) {
  std::string result = "\"";
  for (char c : text) {
    if (c == '"' || c == '\\') result += '\\';
    result += c;
  }
  return result + "\"";
}

std::string Names(const std::set<std::string> &names) {
  std::string result = "[";
  for (const std::string &name : names) result += (result.size() > 1 ? ", " : "") + Quote(name);
  return result + "]";
}

std::string Json(const Summary &s) {
  std::string literals = "[";
  for (const auto &[kind, text] : s.literals) {
    literals += (literals.size() > 1 ? ", " : "") + std::string("[") + Quote(kind) + ", " + Quote(text) + "]";
  }
  literals += "]";
  std::string result = "{\"kind\": " + Quote(s.kind) + ", \"tables\": " + Names(s.tables);
  if (s.kind == "select") {
    result += ", \"select_items\": " + std::to_string(s.select_items) +
              ", \"joins\": " + std::to_string(s.joins) +
              ", \"where\": " + (s.where ? "true" : "false") +
              ", \"group_by\": " + std::to_string(s.group_by) +
              ", \"order_by\": " + std::to_string(s.order_by) +
              ", \"functions\": " + Names(s.functions);
  } else {
    result += ", \"columns\": " + std::to_string(s.columns) + ", \"rows\": " + std::to_string(s.rows);
  }
  return result + ", \"literals\": " + literals + "}";
}

}  // namespace

// Parses every statement of the text; returns 0 and fills summaries when all parse.
int ParseAll(const std::string &text, std::vector<std::string> *summaries) {
  googlesql::ParserOptions options{googlesql::LanguageOptions()};
  googlesql::ParseResumeLocation location = googlesql::ParseResumeLocation::FromString(text);
  bool at_end = false;
  while (!at_end) {
    std::unique_ptr<googlesql::ParserOutput> output;
    absl::Status status = googlesql::ParseNextStatement(&location, options, &output, &at_end);
    if (!status.ok()) {
      std::fprintf(stderr, "%s\n", status.ToString().c_str());
      return 1;
    }
    if (summaries == nullptr) continue;
    const googlesql::ASTStatement *statement = output->statement();
    Summary summary;
    if (statement->GetAsOrNull<googlesql::ASTQueryStatement>() != nullptr) {
      summary.kind = "select";
    } else if (statement->GetAsOrNull<googlesql::ASTInsertStatement>() != nullptr) {
      summary.kind = "insert";
    } else {
      summary.kind = Lower(statement->GetNodeKindString());
    }
    Walk(statement, &summary);
    summaries->push_back(Json(summary));
  }
  return 0;
}

#ifndef PARSARIUM_PROBE
int main(int argc, char **argv) {
  if (argc != 2) return 2;
  FILE *file = std::fopen(argv[1], "rb");
  if (!file) return 2;
  std::vector<char> data(1u << 20);
  size_t size = std::fread(data.data(), 1, data.size(), file);
  std::fclose(file);
  if (size == data.size()) return 2;
  std::vector<std::string> summaries;
  if (ParseAll(std::string(data.data(), size), &summaries) != 0) return 1;
  std::string result = "{\"statement_count\": " + std::to_string(summaries.size()) + ", \"statements\": [";
  for (size_t i = 0; i < summaries.size(); ++i) result += (i ? ", " : "") + summaries[i];
  std::printf("%s]}\n", result.c_str());
  return 0;
}
#endif
