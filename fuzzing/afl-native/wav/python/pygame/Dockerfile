FROM --platform=linux/amd64 aflplusplus/aflplusplus@sha256:d3e2dcafcfbc27bf6b6890e9f9a6e3c420737bb2dc3d8c29d33a76f9c108a090 AS afltools

FROM --platform=linux/amd64 parsarium/wav-python-pygame:local
COPY --from=afltools /usr/local/bin/afl-qemu-trace /opt/afl/bin/afl-qemu-trace
COPY --from=afltools /usr/local/bin/afl-showmap /opt/afl/bin/afl-showmap
COPY --from=afltools /usr/local/bin/afl-fuzz /opt/afl/bin/afl-fuzz
COPY --from=afltools /lib/x86_64-linux-gnu/libpython3.12.so.1.0 /opt/afl/lib/libpython3.12.so.1.0
COPY run-once.py /work/binary-run-once.py
COPY smoke.py /work/binary-smoke.py
ENV AFL_PATH=/opt/afl/bin LD_LIBRARY_PATH=/opt/afl/lib
