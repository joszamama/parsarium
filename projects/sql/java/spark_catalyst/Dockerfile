FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Apache Spark spark-catalyst_2.12 3.5.9 (Apache-2.0). Of its 132-jar Maven runtime closure only the 17 jars the
# CatalystSqlParser path loads are pinned (found by adding the providing jar for each missing class): spark-sql-api
# (ANTLR-generated SqlBaseParser), spark-core, spark-common-utils, spark-unsafe, spark-network-common, Scala 2.12.18,
# antlr4-runtime 4.9.3, hadoop-client-api, log4j, json4s-ast, kryo-shaded, commons-lang3, commons-codec and slf4j-api.
RUN mkdir /work/lib \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/com/esotericsoftware/kryo-shaded/4.0.2/kryo-shaded-4.0.2.jar -o /work/lib/kryo-shaded-4.0.2.jar \
    && echo 'a4899f57fef456b9ec66f730e7b493ecb3dc494cc5758721ed9c18416fd2d3b6  /work/lib/kryo-shaded-4.0.2.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/commons-codec/commons-codec/1.16.1/commons-codec-1.16.1.jar -o /work/lib/commons-codec-1.16.1.jar \
    && echo 'ec87bfb55f22cbd1b21e2190eeda28b2b312ed2a431ee49fbdcc01812d04a5e4  /work/lib/commons-codec-1.16.1.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/antlr/antlr4-runtime/4.9.3/antlr4-runtime-4.9.3.jar -o /work/lib/antlr4-runtime-4.9.3.jar \
    && echo '131a6594969bc4f321d652ea2a33bc0e378ca312685ef87791b2c60b29d01ea5  /work/lib/antlr4-runtime-4.9.3.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar -o /work/lib/commons-lang3-3.12.0.jar \
    && echo 'd919d904486c037f8d193412da0c92e22a9fa24230b9d67a57855c5c31c7e94e  /work/lib/commons-lang3-3.12.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/hadoop/hadoop-client-api/3.3.4/hadoop-client-api-3.3.4.jar -o /work/lib/hadoop-client-api-3.3.4.jar \
    && echo 'e513d71b78086b5caaa439f4402b43e20df01446d56b66084ad419452878701c  /work/lib/hadoop-client-api-3.3.4.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-api/2.20.0/log4j-api-2.20.0.jar -o /work/lib/log4j-api-2.20.0.jar \
    && echo '2f43eea679ea66f14ca0f13fec2a8600ac124f5a5231dcb4df8393eddcb97550  /work/lib/log4j-api-2.20.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/logging/log4j/log4j-core/2.20.0/log4j-core-2.20.0.jar -o /work/lib/log4j-core-2.20.0.jar \
    && echo '6137df848cdaed9f4d5076f75513c6c85da80b953f4e7acca38098b770763f55  /work/lib/log4j-core-2.20.0.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/spark/spark-catalyst_2.12/3.5.9/spark-catalyst_2.12-3.5.9.jar -o /work/lib/spark-catalyst_2.12-3.5.9.jar \
    && echo '58715b96ee0dd847848d8096ea8da8409ee888689dbe71ec1fd07237f0d4d4d1  /work/lib/spark-catalyst_2.12-3.5.9.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/spark/spark-common-utils_2.12/3.5.9/spark-common-utils_2.12-3.5.9.jar -o /work/lib/spark-common-utils_2.12-3.5.9.jar \
    && echo 'f67adc2920421c041c838bd36ef54cf46ae8e114cfb85b8794a220535690b9ad  /work/lib/spark-common-utils_2.12-3.5.9.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/spark/spark-core_2.12/3.5.9/spark-core_2.12-3.5.9.jar -o /work/lib/spark-core_2.12-3.5.9.jar \
    && echo 'f8c2a9001598855b08a8f85adc66a7bec80b0e25109f0149a34e350f9340d788  /work/lib/spark-core_2.12-3.5.9.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/spark/spark-network-common_2.12/3.5.9/spark-network-common_2.12-3.5.9.jar -o /work/lib/spark-network-common_2.12-3.5.9.jar \
    && echo '492fbb14c7d7b82cea26f70c2fcf1f24fef6f7640786d38516dcee1d8c196821  /work/lib/spark-network-common_2.12-3.5.9.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/spark/spark-sql-api_2.12/3.5.9/spark-sql-api_2.12-3.5.9.jar -o /work/lib/spark-sql-api_2.12-3.5.9.jar \
    && echo '9f6ea16201c783c2bfde5e913405b7d9997ad2ebd840a4977f96e82bb7d64544  /work/lib/spark-sql-api_2.12-3.5.9.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/spark/spark-unsafe_2.12/3.5.9/spark-unsafe_2.12-3.5.9.jar -o /work/lib/spark-unsafe_2.12-3.5.9.jar \
    && echo '13463c25d402f1c63caa7a0fca3bc0a055b048b0f5948cf363234b301c35d548  /work/lib/spark-unsafe_2.12-3.5.9.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/json4s/json4s-ast_2.12/3.7.0-M11/json4s-ast_2.12-3.7.0-M11.jar -o /work/lib/json4s-ast_2.12-3.7.0-M11.jar \
    && echo 'f9388c0ad4a969bf1a1867e85ce24ed87ca5a1095342b96b35c356fd971b544d  /work/lib/json4s-ast_2.12-3.7.0-M11.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/scala-lang/scala-library/2.12.18/scala-library-2.12.18.jar -o /work/lib/scala-library-2.12.18.jar \
    && echo 'e51e6636c003359e106bea4ad99def70e613c290190c8c84f10f9560dd5b00ae  /work/lib/scala-library-2.12.18.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/scala-lang/scala-reflect/2.12.18/scala-reflect-2.12.18.jar -o /work/lib/scala-reflect-2.12.18.jar \
    && echo 'd6a24e175246541ffcbc965a231aa1d3bb01d61def196f91495690fabf9783bc  /work/lib/scala-reflect-2.12.18.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/slf4j/slf4j-api/1.7.36/slf4j-api-1.7.36.jar -o /work/lib/slf4j-api-1.7.36.jar \
    && echo 'd3ef575e3e4979678dc01bf1dcce51021493b4d11fb7f1be8ad982877c16a1c0  /work/lib/slf4j-api-1.7.36.jar' | sha256sum --check
# Coverage subject: Spark's org.apache.spark.sql.catalyst classes from spark-catalyst (AstBuilder, CatalystSqlParser, logical plans, expressions) and spark-sql-api (ANTLR-generated SqlBaseLexer and SqlBaseParser).
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/spark/spark-catalyst_2.12/3.5.9/spark-catalyst_2.12-3.5.9-sources.jar -o /work/parser-sources.jar \
    && echo '960ca5e1ac07625063855be2e552202d1e84d069f288e51d5ad08bb0fa685a7d  /work/parser-sources.jar' | sha256sum --check \
    && mkdir /work/parser-source /work/parser-classes \
    && unzip -q /work/parser-sources.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -q /work/lib/spark-catalyst_2.12-3.5.9.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class' \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/apache/spark/spark-sql-api_2.12/3.5.9/spark-sql-api_2.12-3.5.9-sources.jar -o /work/extra-sources-0.jar \
    && echo '8ac6cb5826cfc3d201c0faaf0a181bde75c954b2abac9a13bd49b3cd5412bd29  /work/extra-sources-0.jar' | sha256sum --check \
    && unzip -qo /work/extra-sources-0.jar -d /work/parser-source -x 'META-INF/*' \
    && unzip -qo /work/lib/spark-sql-api_2.12-3.5.9.jar -d /work/parser-classes -x 'META-INF/*' 'module-info.class' \
    && test -f /work/parser-source/org/apache/spark/sql/catalyst/parser/AstBuilder.scala
RUN curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.agent/0.8.14/org.jacoco.agent-0.8.14-runtime.jar -o /work/jacocoagent.jar \
    && echo '3fb76eea65f81bd9415202bab34b6571728841dff1ab8e6bbe81adc2e299face  /work/jacocoagent.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://repo.maven.apache.org/maven2/org/jacoco/org.jacoco.cli/0.8.14/org.jacoco.cli-0.8.14-nodeps.jar -o /work/jacococli.jar \
    && echo '811c7f8c6b358c5d68a8973cfa867f6892be7a671b697a4b13c4b447e6daf75c  /work/jacococli.jar' | sha256sum --check \
    && curl --fail --location --retry 3 https://github.com/CodeIntelligenceTesting/jazzer/releases/download/v0.26.0/jazzer-linux-arm64.tar.gz -o /work/jazzer.tar.gz \
    && echo '0ad74e5d67f7f7a3c8453f7dd5030d4bce5aae6e47c3e2b8ebc98699244c7e4f  /work/jazzer.tar.gz' | sha256sum --check \
    && tar -xf /work/jazzer.tar.gz -C /work
COPY SqlHarness.java /work/src/
RUN mkdir /work/classes && javac -cp '/work/lib/*' -d /work/classes /work/src/*.java \
    && { java -version 2>&1 | head -1; /work/jazzer --version 2>&1 | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 eclipse-temurin@sha256:b8705e936964c228dfce359e63dbf08f6c69cb380ed1d576b1f6b1064f15567d
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
# Spark's SQL configuration defaults resolve the local host name when first loaded; these documented
# variables supply it so the parser runs without name resolution (containers run with --network none).
ENV SPARK_LOCAL_HOSTNAME=localhost SPARK_LOCAL_IP=127.0.0.1
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
