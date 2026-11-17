#!/bin/sh
# Build the JaCoCo coverage subject for hive-exec's HiveQL parser.
# hive-parser-4.2.1-sources.jar ships the hand-written parser classes and the ANTLR grammars,
# but not the Java that ANTLR generates from them. This script regenerates that Java with the
# pinned ANTLR 3.5.2 tool, recompiles it with line tables and requires every generated class's
# line numbers to equal those of the class shipped in hive-exec, then extracts the shipped
# classes that have a source file into /work/parser-classes.
set -eu
SRC=/work/parser-source/org/apache/hadoop/hive/ql/parse
GEN=/work/antlr-gen
mkdir -p "$GEN" /work/recompiled /work/parser-classes
cp "$SRC"/*.g "$GEN"/
for grammar in HiveLexerParent HiveLexer HiveLexerStandard HiveParser HintParser; do
  java -cp /work/antlr-complete-3.5.2.jar org.antlr.Tool -lib "$GEN" -o "$GEN" -fo "$GEN" "$GEN/$grammar.g" 2>&1 \
    | grep -v '^warning' || true
done
# HiveLexerParent is only an imported grammar; hive-exec ships no HiveLexerParent class.
rm -f "$GEN/HiveLexerParent.java"
cp "$GEN"/*.java "$SRC"/
javac -nowarn -g -implicit:none -sourcepath /work/parser-source -cp '/work/lib/*' -d /work/recompiled "$GEN"/*.java
checked=0
for file in "$GEN"/*.java; do
  class=org.apache.hadoop.hive.ql.parse.$(basename "$file" .java)
  shipped=$(javap -l -p -cp /work/lib/hive-exec-4.2.1.jar "$class" | grep -o 'line [0-9]*' | md5sum)
  rebuilt=$(javap -l -p -cp /work/recompiled "$class" | grep -o 'line [0-9]*' | md5sum)
  [ "$shipped" = "$rebuilt" ] || { echo "line table differs: $class" >&2; exit 1; }
  checked=$((checked + 1))
done
echo "generated classes with matching line tables: $checked"
cd /work/parser-source
find . -name '*.java' | sed 's|^\./||; s|\.java$||' > /work/source-classes.txt
cd /work/parser-classes
while read -r name; do
  unzip -qo /work/lib/hive-exec-4.2.1.jar "$name.class" "$name\$*.class" 2>/dev/null || true
done < /work/source-classes.txt
test -f /work/parser-classes/org/apache/hadoop/hive/ql/parse/HiveParser.class
test -f /work/parser-classes/org/apache/hadoop/hive/ql/parse/ParseDriver.class
rm -rf "$GEN" /work/recompiled
