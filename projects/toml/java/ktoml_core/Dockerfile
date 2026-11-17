FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# ktoml-core-jvm 0.7.1 and the runtime dependencies its release POM declares (kotlin-stdlib 2.2.0,
# kotlinx-serialization-core-jvm 1.9.0, kotlinx-datetime-jvm 0.7.1-0.6.x-compat).
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/akuleshov7/ktoml-core-jvm/0.7.1/ktoml-core-jvm-0.7.1.jar -o /work/lib/ktoml-core-jvm-0.7.1.jar \
    && echo 'c22cb661eefc75e30007a1b08d37c4e93a157f7f3a950a478251632c0af6050d  /work/lib/ktoml-core-jvm-0.7.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/2.2.0/kotlin-stdlib-2.2.0.jar -o /work/lib/kotlin-stdlib-2.2.0.jar \
    && echo '65d12d85a3b865c160db9147851712a64b10dadd68b22eea22a95bf8a8670dca  /work/lib/kotlin-stdlib-2.2.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlinx/kotlinx-serialization-core-jvm/1.9.0/kotlinx-serialization-core-jvm-1.9.0.jar -o /work/lib/kotlinx-serialization-core-jvm-1.9.0.jar \
    && echo '1f0afa172110e45a7231ef1b44ae8fd84c1ebaff96f3fc3ad68ef8c48120b59c  /work/lib/kotlinx-serialization-core-jvm-1.9.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jetbrains/kotlinx/kotlinx-datetime-jvm/0.7.1-0.6.x-compat/kotlinx-datetime-jvm-0.7.1-0.6.x-compat.jar -o /work/lib/kotlinx-datetime-jvm-0.7.1-0.6.x-compat.jar \
    && echo 'cf9cdf7b3074044657a1a80bc1bb5280b58545a967ac7fe42b1aa3cf93305714  /work/lib/kotlinx-datetime-jvm-0.7.1-0.6.x-compat.jar' | sha256sum --check
# Coverage subject: the ktoml-core-jvm release jar and its release sources jar only. The Kotlin
# multiplatform sources jar keeps files under commonMain/ and jvmMain/ by directory, and some files
# sit in a directory that differs from their package (tree/nodes/tables/TomlTable.kt is in package
# com.akuleshov7.ktoml.tree.nodes), so each .kt file is placed by its own package declaration.
RUN mkdir /work/parser-source /work/parser-classes /work/ktoml-sources \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/akuleshov7/ktoml-core-jvm/0.7.1/ktoml-core-jvm-0.7.1-sources.jar -o /work/ktoml-sources.jar \
    && echo '837ca4a05eb4ed21a192df6ac1f2d6c7a55e6407d19f90ec2fce98843d6d4ee1  /work/ktoml-sources.jar' | sha256sum --check \
    && unzip -q -o /work/ktoml-sources.jar -d /work/ktoml-sources -x 'META-INF/*' \
    && for file in $(find /work/ktoml-sources -name '*.kt' | sort); do \
         package=$(sed -n 's/^package \([A-Za-z0-9_.]*\).*/\1/p' "$file" | head -1 | tr . /); \
         test -n "$package"; target="/work/parser-source/$package/$(basename "$file")"; \
         test ! -e "$target"; mkdir -p "$(dirname "$target")"; cp "$file" "$target"; \
       done \
    && unzip -q -o /work/lib/ktoml-core-jvm-0.7.1.jar -d /work/parser-classes -x 'META-INF/*'
# Three classes in ktoml's packages are kotlin-stdlib inline lambdas (filterIsInstance iterators and
# a sortBy comparator) whose SourceFile is the stdlib's _Sequences.kt or Comparisons.kt; they are
# outside the parser-source subject. They stay in the runtime jar; only the JaCoCo class directory
# omits them. Any other class without a ktoml source file fails the build.
RUN cd /work/parser-classes && for class in $(find . -name '*.class' | sort); do \
         source=$(javap -v "$class" | sed -n 's/^SourceFile: "\(.*\)"/\1/p'); \
         test -f "/work/parser-source/$(dirname "$class")/$source" || { echo "$class $source"; rm "$class"; }; \
       done > /work/parser-classes-excluded.txt \
    && printf '%s\n' \
         './com/akuleshov7/ktoml/encoders/TomlMainEncoder$endStructure$$inlined$sortBy$1.class Comparisons.kt' \
         './com/akuleshov7/ktoml/tree/nodes/TomlNode$findTableInAstByName$$inlined$filterIsInstance$1.class _Sequences.kt' \
         './com/akuleshov7/ktoml/tree/nodes/TomlNode$findTableInAstByName$$inlined$filterIsInstance$2.class _Sequences.kt' \
       | cmp - /work/parser-classes-excluded.txt
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY TomlAdapter.java GenericHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/classes /work/classes
COPY --from=build /work/lib /work/lib
COPY --from=build /work/parser-source /work/parser-source
COPY --from=build /work/parser-classes /work/parser-classes
COPY --from=build /work/jacocoagent.jar /work/jacococli.jar /work/jazzer /work/jazzer_standalone.jar /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
