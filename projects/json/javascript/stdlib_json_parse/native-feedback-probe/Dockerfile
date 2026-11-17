FROM parsarium/json-javascript-stdlib_json_parse:local
RUN apt-get update -qq && apt-get install -y --no-install-recommends gdb binutils \
    && rm -rf /var/lib/apt/lists/* \
    && gdb --version | head -n 1 > /work/gdb-version.txt
COPY probe.py probe.sh /work/
ENTRYPOINT ["sh", "/work/probe.sh"]
