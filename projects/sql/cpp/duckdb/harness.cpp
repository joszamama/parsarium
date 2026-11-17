// DuckDB: duckdb::Parser::ParseQuery(local SQL text) fills Parser::statements with SQLStatement
// trees (SelectStatement/SelectNode, InsertStatement/InsertQueryNode, TableRef and ParsedExpression
// nodes). The replay walks those trees and prints the oracle summary as one JSON line.
// No database, connection or client context is created; nothing is bound or executed.
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <set>
#include <string>
#include <utility>
#include <vector>

#include "duckdb/parser/parser.hpp"
#include "duckdb/parser/parsed_expression_iterator.hpp"
#include "duckdb/parser/expression/constant_expression.hpp"
#include "duckdb/parser/expression/function_expression.hpp"
#include "duckdb/parser/query_node/select_node.hpp"
#include "duckdb/parser/query_node/insert_query_node.hpp"
#include "duckdb/parser/statement/select_statement.hpp"
#include "duckdb/parser/statement/insert_statement.hpp"
#include "duckdb/parser/tableref/basetableref.hpp"
#include "duckdb/parser/tableref/joinref.hpp"
#include "duckdb/parser/tableref/expressionlistref.hpp"
#include "duckdb/parser/result_modifier.hpp"

using namespace duckdb;

namespace {

std::string lower(std::string text) {
    std::transform(text.begin(), text.end(), text.begin(),
                   [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
    return text;
}

std::string quote(const std::string &text) {
    std::string out = "\"";
    for (unsigned char c : text) {
        if (c == '"' || c == '\\') { out += '\\'; out += static_cast<char>(c); }
        else if (c < 0x20) { char buf[8]; std::snprintf(buf, sizeof buf, "\\u%04x", c); out += buf; }
        else out += static_cast<char>(c);
    }
    return out + "\"";
}

std::string names(const std::set<std::string> &items) {
    std::string out = "[";
    for (auto it = items.begin(); it != items.end(); ++it) out += (it == items.begin() ? "" : ",") + quote(*it);
    return out + "]";
}

struct Facts {
    std::set<std::string> tables, functions;
    std::vector<std::pair<std::string, std::string>> literals;
    int joins = 0;
};

// Records function names and literals of one parsed expression and all its children.
void visit_expression(const ParsedExpression &expression, Facts &facts) {
    if (expression.GetExpressionClass() == ExpressionClass::FUNCTION) {
        auto name = lower(expression.Cast<FunctionExpression>().FunctionName().GetIdentifierName());
        // DuckDB's transformer stores COUNT(*) as the zero-argument function "count_star".
        facts.functions.insert(name == "count_star" ? "count" : name);
    } else if (expression.GetExpressionClass() == ExpressionClass::CONSTANT) {
        const Literal &literal = expression.Cast<ConstantExpression>().GetLiteral();
        if (literal.kind == LiteralKind::STRING) facts.literals.emplace_back("string", literal.text);
        else if (literal.kind == LiteralKind::INTEGER || literal.kind == LiteralKind::NUMERIC)
            facts.literals.emplace_back("number", literal.text);
    }
    ParsedExpressionIterator::EnumerateChildren(
        expression, [&](const ParsedExpression &child) { visit_expression(child, facts); });
}

// Records base tables and join operators of a FROM tree, and the expressions inside it.
void visit_table(TableRef &ref, Facts &facts) {
    if (ref.type == TableReferenceType::BASE_TABLE) {
        facts.tables.insert(lower(ref.Cast<BaseTableRef>().Table().GetIdentifierName()));
    } else if (ref.type == TableReferenceType::JOIN) {
        auto &join = ref.Cast<JoinRef>();
        facts.joins++;
        visit_table(*join.left, facts);
        visit_table(*join.right, facts);
        if (join.condition) visit_expression(*join.condition, facts);
    }
}

std::string literals_json(Facts &facts) {
    std::sort(facts.literals.begin(), facts.literals.end());
    std::string out = "[";
    for (size_t i = 0; i < facts.literals.size(); i++)
        out += (i ? "," : "") + std::string("[") + quote(facts.literals[i].first) + "," + quote(facts.literals[i].second) + "]";
    return out + "]";
}

std::string summarize(SQLStatement &statement) {
    Facts facts;
    if (statement.type == StatementType::SELECT_STATEMENT) {
        auto &node = *statement.Cast<SelectStatement>().node;
        if (node.type != QueryNodeType::SELECT_NODE) return "{\"kind\":\"select_other\"}";
        auto &select = node.Cast<SelectNode>();
        for (auto &item : select.select_list) visit_expression(*item, facts);
        if (select.from_table) visit_table(*select.from_table, facts);
        if (select.where_clause) visit_expression(*select.where_clause, facts);
        for (auto &group : select.groups.group_expressions) visit_expression(*group, facts);
        size_t order_by = 0;
        for (auto &modifier : select.modifiers) {
            if (modifier->type != ResultModifierType::ORDER_MODIFIER) continue;
            auto &orders = modifier->Cast<OrderModifier>().orders;
            order_by += orders.size();
            for (auto &order : orders) visit_expression(*order.expression, facts);
        }
        return "{\"kind\":\"select\",\"tables\":" + names(facts.tables) +
               ",\"select_items\":" + std::to_string(select.select_list.size()) +
               ",\"joins\":" + std::to_string(facts.joins) +
               ",\"where\":" + (select.where_clause ? "true" : "false") +
               ",\"group_by\":" + std::to_string(select.groups.group_expressions.size()) +
               ",\"order_by\":" + std::to_string(order_by) +
               ",\"functions\":" + names(facts.functions) + ",\"literals\":" + literals_json(facts) + "}";
    }
    if (statement.type == StatementType::INSERT_STATEMENT) {
        auto &insert = *statement.Cast<InsertStatement>().node;
        auto values = insert.GetValuesList();
        size_t rows = 0;
        if (values) {
            rows = values->values.size();
            for (auto &row : values->values)
                for (auto &item : row) visit_expression(*item, facts);
        }
        std::set<std::string> table = {lower(insert.qualified_name.Name().GetIdentifierName())};
        return "{\"kind\":\"insert\",\"tables\":" + names(table) +
               ",\"columns\":" + std::to_string(insert.columns.size()) + ",\"rows\":" + std::to_string(rows) +
               ",\"literals\":" + literals_json(facts) + "}";
    }
    return "{\"kind\":\"other\"}";
}

bool text_from(const uint8_t *data, size_t size, std::string &text) {
    if (!data || size == 0 || size > (1u << 20) || std::memchr(data, 0, size)) return false;
    text.assign(reinterpret_cast<const char *>(data), size);
    return true;
}

} // namespace

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    std::string text;
    if (!text_from(data, size, text)) return 0;
    try {
        Parser parser = Parser::GetBuiltinParser();
        parser.ParseQuery(text);
    } catch (std::exception &) {
    }
    return 0;
}

#ifndef PARSARIUM_FUZZER
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    FILE *file = std::fopen(argv[1], "rb");
    if (!file) return 3;
    std::vector<uint8_t> data((1u << 20) + 1);
    size_t size = std::fread(data.data(), 1, data.size(), file);
    std::fclose(file);
    std::string text;
    if (!text_from(data.data(), size, text)) return 4;
    try {
        Parser parser = Parser::GetBuiltinParser();
        parser.ParseQuery(text);
        std::string out = "{\"statement_count\":" + std::to_string(parser.statements.size()) + ",\"statements\":[";
        for (size_t i = 0; i < parser.statements.size(); i++) out += (i ? "," : "") + summarize(*parser.statements[i]);
        std::puts((out + "]}").c_str());
    } catch (std::exception &error) {
        std::fprintf(stderr, "parse error: %s\n", error.what());
        return 5;
    }
    return 0;
}
#endif
