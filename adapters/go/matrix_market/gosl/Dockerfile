FROM ubuntu:24.04@sha256:2198e4c65076e9cb0b3d695219df667c0e3b0072da64ca3c2648aca17dcecaf5

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates=20260816ubuntu0.24.04.2 \
    gcc=4:13.2.0-7ubuntu1 \
    gfortran=4:13.2.0-7ubuntu1 \
    golang-go=2:1.22~2build1 \
    libfftw3-dev=3.3.10-1ubuntu3 \
    liblapacke-dev=3.12.0-3build1.1 \
    libmetis-dev=5.1.0.dfsg-7build3 \
    libmumps-seq-dev=5.6.2-2.1build2 \
    libopenblas-dev=0.3.26+ds-1ubuntu0.1 \
    libsuitesparse-dev=1:7.6.1+dfsg-1build1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /repo/adapters/go/matrix_market/gosl
