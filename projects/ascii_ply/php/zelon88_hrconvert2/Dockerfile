FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-xdebug python3 python3-venv assimp-utils=6.0.4+ds-1build1 unzip \
    libgl1 libopengl0 libp11-kit0 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-interaction --no-progress --prefer-dist
RUN mkdir -p /work/wheels /work/parser/Resources/Pipelines/Model \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/79/c0/9b769a1acd7ce4405059820793c2f14129d9faba99b595ea35c8c9d8c57d/pymeshlab-2025.7.post1-cp314-cp314-manylinux_2_35_x86_64.whl --output /work/wheels/pymeshlab-2025.7.post1-cp314-cp314-manylinux_2_35_x86_64.whl \
    && echo '951fe5aeb3e92632f3db3a1a6525279b41e5d7191c6b9011429dbb0b67f2f0d3  /work/wheels/pymeshlab-2025.7.post1-cp314-cp314-manylinux_2_35_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl \
    && curl --fail --location --retry 3 https://raw.githubusercontent.com/zelon88/HRConvert2/v4.0.0/Resources/Pipelines/Model/pipeline.php --output /work/parser/Resources/Pipelines/Model/pipeline.php \
    && echo '7e5018273402f38fc61c9e17d34238dbbc038a1d27b9373e24e6689df4c7bd09  /work/parser/Resources/Pipelines/Model/pipeline.php' | sha256sum --check
ENV PATH=/opt/venv/bin:$PATH PARSARIUM_PYTHON=/opt/venv/bin/python3 PARSARIUM_ASSIMP=/usr/bin/assimp QT_QPA_PLATFORM=offscreen
RUN { php --version | head -1; composer --version; /opt/venv/bin/python -c 'import pymeshlab; print("PyMeshLab", pymeshlab.__version__ if hasattr(pymeshlab,"__version__") else "2025.7.post1")'; assimp version | head -1; } > /work/toolchain.txt
COPY harness.php fuzz-target.php run-control.php /work/
ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/run-control.php"]
