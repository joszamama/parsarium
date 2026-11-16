FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/8f/1a/819a16215a5844ea9aa9922009f9b4147b38d8c40e169af7052e743fbaa9/open3d-0.20.0-cp314-cp314-manylinux_2_35_x86_64.whl --output /work/wheels/open3d-0.20.0-cp314-cp314-manylinux_2_35_x86_64.whl \
    && echo '14e0928af6f83555e58dde934af85fe61f6f9f5160f883e6e720d6205c38c68a  /work/wheels/open3d-0.20.0-cp314-cp314-manylinux_2_35_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/99/91/8acff4f5e50511b911bbccb72b8628a49c68ce14148cd9f6431094859a90/annotated_types-0.8.0-py3-none-any.whl --output /work/wheels/annotated_types-0.8.0-py3-none-any.whl \
    && echo 'f072f4d804ea359e4eaf198b1af7a8b0943881a87f31bb764f8bf219bb9419e0  /work/wheels/annotated_types-0.8.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/d4/2b/04b8a15f3a1c77bc79ddf5c73875327f34b4fa75982df2b76e45e402d364/asttokens-3.0.2-py3-none-any.whl --output /work/wheels/asttokens-3.0.2-py3-none-any.whl \
    && echo '9da13157f5b28becde0bd374fc677dcd3c290614264eff096f167c469cd9f933  /work/wheels/asttokens-3.0.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/64/b4/17d4b0b2a2dc85a6df63d1157e028ed19f90d4cd97c36717afef2bc2f395/attrs-26.1.0-py3-none-any.whl --output /work/wheels/attrs-26.1.0-py3-none-any.whl \
    && echo 'c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309  /work/wheels/attrs-26.1.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/10/cb/f2ad4230dc2eb1a74edf38f1a38b9b52277f75bef262d8908e60d957e13c/blinker-1.9.0-py3-none-any.whl --output /work/wheels/blinker-1.9.0-py3-none-any.whl \
    && echo 'ba0efaa9080b619ff2f3459d1d500c57bddea4a6b424b60a91141db6fd2f08bc  /work/wheels/blinker-1.9.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/32/d1/a3652fe2c19134d0d15922177821d863cbd7e842d53a21bbe7e8e3a1b5ac/certifi-2026.10.23-py3-none-any.whl --output /work/wheels/certifi-2026.10.23-py3-none-any.whl \
    && echo 'e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1  /work/wheels/certifi-2026.10.23-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/fc/ad/d07d7862a62ffa6d79d68074d14823243dd235a77c45262acbf6adeb28bf/charset_normalizer-3.5.2-py3-none-any.whl --output /work/wheels/charset_normalizer-3.5.2-py3-none-any.whl \
    && echo 'b6b751274acb69d77b3323d6b7dbaa3c7fdfc1eb829b7eb61d262f32e1af9685  /work/wheels/charset_normalizer-3.5.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/31/7d/164b7ffc8624fe9efb4221bf9af485d5c1e41b9ae118045d2b6dc5457d8b/click-8.5.1-py3-none-any.whl --output /work/wheels/click-8.5.1-py3-none-any.whl \
    && echo '8bb5376d2006950386f8c6427613334a2acadc5f559cb80e638d00b4df957e37  /work/wheels/click-8.5.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/60/97/891a0971e1e4a8c5d2b20bbe0e524dc04548d2307fee33cdeba148fd4fc7/comm-0.2.3-py3-none-any.whl --output /work/wheels/comm-0.2.3-py3-none-any.whl \
    && echo 'c615d91d75f7f04f095b30d1c1711babd43bdc6419c1be9886a85f2f4e489417  /work/wheels/comm-0.2.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/bd/de/f7fe2171f2b650ef7dd455c4c7f6dbaf53cc942430a2e0ff6b2450e728b5/configargparse-1.9.0-py3-none-any.whl --output /work/wheels/configargparse-1.9.0-py3-none-any.whl \
    && echo 'e4ecc54d821ca97c43e6152403f40e158aff79d809c3447746fa92b136dc1e31  /work/wheels/configargparse-1.9.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b3/77/36799a6b840c0d6acf726ad06a9e10355827f9c84f506d0ba168238ba54c/dash-4.5.0-py3-none-any.whl --output /work/wheels/dash-4.5.0-py3-none-any.whl \
    && echo 'd50a0900c2ce9e5f43f484d6966acc3ecbddcfd54df727311e34a0b7d3da2129  /work/wheels/dash-4.5.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/4d/dd/8bc67e7d5ffc1d88aa5af511189dfb76dc4e1e5b808fab186146ef2663e5/executing-2.3.0-py3-none-any.whl --output /work/wheels/executing-2.3.0-py3-none-any.whl \
    && echo '736e859c9f8701f11fcf516856f26f562e04776387824b43a35a1dfe21c84122  /work/wheels/executing-2.3.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/d7/0d/6caab33488dc9d26440c24221fa610c7c8b83c30715ab45d31f0e004308e/fastjsonschema-2.22.3-py3-none-any.whl --output /work/wheels/fastjsonschema-2.22.3-py3-none-any.whl \
    && echo 'f670b443830b75aca3f00b75949efa20f4b2a80302ec7a21505c28dd54cffd43  /work/wheels/fastjsonschema-2.22.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/7f/9c/34f6962f9b9e9c71f6e5ed806e0d0ff03c9d1b0b2340088a0cf4bce09b18/flask-3.1.3-py3-none-any.whl --output /work/wheels/flask-3.1.3-py3-none-any.whl \
    && echo 'f4bcbefc124291925f1a26446da31a5178f9483862233b23c0c96a20701f670c  /work/wheels/flask-3.1.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/58/a2/bb081bab032533a855d44de1d56f8e8426114ff1ba5d1f07a438a0a654f8/idna-3.20-py3-none-any.whl --output /work/wheels/idna-3.20-py3-none-any.whl \
    && echo 'ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c  /work/wheels/idna-3.20-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/7f/61/0c0fae37eb561d8fddb788cbae0f227051628d70d67498a8a116c1f547d7/importlib_metadata-10.2.0-py3-none-any.whl --output /work/wheels/importlib_metadata-10.2.0-py3-none-any.whl \
    && echo 'c7a4bf1c7479601f6b8e437cfc14f4f77028ba62a8f34ae95cd93d9774dfba51  /work/wheels/importlib_metadata-10.2.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/bb/1c/91da4a1c541b75e97eb99d09c6a9b0534de55bb4a466669d1170e39b915c/ipython-9.18.1-py3-none-any.whl --output /work/wheels/ipython-9.18.1-py3-none-any.whl \
    && echo '997ce9140d374531a61069c70c0f9ef299d6dd3559ea0f94b8af589726e3c1d5  /work/wheels/ipython-9.18.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/d9/33/1f075bf72b0b747cb3288d011319aaf64083cf2efef8354174e3ed4540e2/ipython_pygments_lexers-1.1.1-py3-none-any.whl --output /work/wheels/ipython_pygments_lexers-1.1.1-py3-none-any.whl \
    && echo 'a9462224a505ade19a605f71f8fa63c2048833ce50abc86768a0d81d876dc81c  /work/wheels/ipython_pygments_lexers-1.1.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/55/298e9b3b864a198234997e87a1471c1b17d7f3546ace6d18fb5cf1ce24b2/ipywidgets-8.1.9-py3-none-any.whl --output /work/wheels/ipywidgets-8.1.9-py3-none-any.whl \
    && echo 'f2b8cbcaae10252b809fbe4d7470db75c09b769a32cbf816d20e5ca6d3c5a79d  /work/wheels/ipywidgets-8.1.9-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/04/96/92447566d16df59b2a776c0fb82dbc4d9e07cd95062562af01e408583fc4/itsdangerous-2.2.0-py3-none-any.whl --output /work/wheels/itsdangerous-2.2.0-py3-none-any.whl \
    && echo 'c6242fc49e35958c8b15141343aa660db5fc54d4f13a1db01a3f5891b98700ef  /work/wheels/itsdangerous-2.2.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/68/34/65604740edcb20e1bda6a890348ed7d282e7dd23aa00401cbe36fd0edbd9/janus-2.0.0-py3-none-any.whl --output /work/wheels/janus-2.0.0-py3-none-any.whl \
    && echo '7e6449d34eab04cd016befbd7d8c0d8acaaaab67cb59e076a69149f9031745f9  /work/wheels/janus-2.0.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/be/c7/71eb0d51cdcbb63b857c931aa4e9218b078b5d9f8ecd383b234f28fe7b0f/jedi-0.20.1-py2.py3-none-any.whl --output /work/wheels/jedi-0.20.1-py2.py3-none-any.whl \
    && echo '0fb16d86c4a4c73c37ba518c77419975e30fcc620658a8d14fbb5720cdd34142  /work/wheels/jedi-0.20.1-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/62/a1/3d680cbfd5f4b8f15abc1d571870c5fc3e594bb582bc3b64ea099db13e56/jinja2-3.1.6-py3-none-any.whl --output /work/wheels/jinja2-3.1.6-py3-none-any.whl \
    && echo '85ece4451f492d0c13c5dd7c13a64681a86afae63a5f347908daf103ce6d2f67  /work/wheels/jinja2-3.1.6-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/69/90/f63fb5873511e014207a475e2bb4e8b2e570d655b00ac19a9a0ca0a385ee/jsonschema-4.26.0-py3-none-any.whl --output /work/wheels/jsonschema-4.26.0-py3-none-any.whl \
    && echo 'd489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce  /work/wheels/jsonschema-4.26.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/41/45/1a4ed80516f02155c51f51e8cedb3c1902296743db0bbc66608a0db2814f/jsonschema_specifications-2025.9.1-py3-none-any.whl --output /work/wheels/jsonschema_specifications-2025.9.1-py3-none-any.whl \
    && echo '98802fee3a11ee76ecaca44429fda8a41bff98b00a0f2838151b113f210cc6fe  /work/wheels/jsonschema_specifications-2025.9.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e7/e7/80988e32bf6f73919a113473a604f5a8f09094de312b9d52b79c2df7612b/jupyter_core-5.9.1-py3-none-any.whl --output /work/wheels/jupyter_core-5.9.1-py3-none-any.whl \
    && echo 'ebf87fdc6073d142e114c72c9e29a9d7ca03fad818c5d300ce2adc1fb0743407  /work/wheels/jupyter_core-5.9.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/33/ef/6d27fc118f58cb24886da413545a7efb0853d405fddbfd8b2d9ac09fbed4/jupyterlab_widgets-3.0.17-py3-none-any.whl --output /work/wheels/jupyterlab_widgets-3.0.17-py3-none-any.whl \
    && echo '40ac1e9955acf116c4d995d9bfa082d86ad9ec6d91c4f134827cf5e0a5eb75e0  /work/wheels/jupyterlab_widgets-3.0.17-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/0a/28/7ded071d0975dcc6d5d106ffbf7b3ca420f7caa3b8a235fa604b6e37032a/lazy_importer-0.1.0-py3-none-any.whl --output /work/wheels/lazy_importer-0.1.0-py3-none-any.whl \
    && echo 'bd93fab7bef18e842eea02b839410954d37889140dc64ca4d9680aec6880c739  /work/wheels/lazy_importer-0.1.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/8f/db/d7282caf7ab03af44d5d6fdbaa019b35c7d7f1c90588b839c07cba640d6a/markupsafe-3.0.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/markupsafe-3.0.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'a8e9f292fcda89b324f2f5c91d13f1424a153e40fc2756f38ee23b15835ff300  /work/wheels/markupsafe-3.0.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/41/09/5b161152e2d90f7b87f781c2e1267494aef9c32498df793f73ad0a0a494a/matplotlib_inline-0.2.2-py3-none-any.whl --output /work/wheels/matplotlib_inline-0.2.2-py3-none-any.whl \
    && echo '3c821cf1c209f59fb2d2d64abbf5b23b67bcb2210d663f9918dd851c6da1fcf6  /work/wheels/matplotlib_inline-0.2.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/cf/82/8ef9c7e0f50493307a49c09cfa7f00c5a778b6d1921f7b2dabe1d3a5809e/narwhals-2.28.0-py3-none-any.whl --output /work/wheels/narwhals-2.28.0-py3-none-any.whl \
    && echo '1f69d6385ec30e2fa6e1fdeb37c562ecabd0f713f6f3e3b58a668c5c9df9567f  /work/wheels/narwhals-2.28.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/1a/69/ee613f74085ca7103f79cd08d579c4f3177d1d26e5d3d9528d2d6536a707/nbformat-5.11.1-py3-none-any.whl --output /work/wheels/nbformat-5.11.1-py3-none-any.whl \
    && echo 'cc6698fa75f4fab8755ead786317815f13a6fee3b53311c0abb1a8b51d52f7ec  /work/wheels/nbformat-5.11.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a0/c4/c2971a3ba4c6103a3d10c4b0f24f461ddc027f0f09763220cf35ca1401b3/nest_asyncio-1.6.0-py3-none-any.whl --output /work/wheels/nest_asyncio-1.6.0-py3-none-any.whl \
    && echo '87af6efd6b5e897c81050477ef65c62e2b2f35d51703cae01aff2905b1852e1c  /work/wheels/nest_asyncio-1.6.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/63/34/ba1c580383c9eada3711951fef0795c80b829a078d72188184bcab9dd527/packaging-26.3-py3-none-any.whl --output /work/wheels/packaging-26.3-py3-none-any.whl \
    && echo 'd7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c  /work/wheels/packaging-26.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/99/5d/8268b644392ee874ee82a635cd0df1773de230bde356c38de28e298392cc/parso-0.8.7-py2.py3-none-any.whl --output /work/wheels/parso-0.8.7-py2.py3-none-any.whl \
    && echo 'a8926eb2a1b915486941fdbd31e86a4baf88fe8c210f25f2f35ecec5b574ca1c  /work/wheels/parso-0.8.7-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/9e/c3/059298687310d527a58bb01f3b1965787ee3b40dce76752eda8b44e9a2c5/pexpect-4.9.0-py2.py3-none-any.whl --output /work/wheels/pexpect-4.9.0-py2.py3-none-any.whl \
    && echo '7236d1e080e4936be2dc3e326cec0af72acf9212a7e1d060210e70a47e253523  /work/wheels/pexpect-4.9.0-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/7c/ae/ecbbbfd0e4343a6a521d49b3c8656fb4643dee2a4f6eaf941cf3280391a8/platformdirs-4.14.5-py3-none-any.whl --output /work/wheels/platformdirs-4.14.5-py3-none-any.whl \
    && echo '8e778c6fa421516f4d3369449f8df3b0e1b72c0e0005fe88e3ec772d0a14e750  /work/wheels/platformdirs-4.14.5-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e5/7d/905a3a3d51087515719058c94cfbda2ff0fc14417c20d557ae3e82d8b250/plotly-7.1.0-py3-none-any.whl --output /work/wheels/plotly-7.1.0-py3-none-any.whl \
    && echo 'dbb7fa18afce40d0a8e80d1bf162eceb3faa0ce5a77fe741ad09a74cf78f53f3  /work/wheels/plotly-7.1.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/54/6f/84908cad2d6aa5144abcf7b42709fe4fdb459bc640ec7ac5786e7693dabc/prompt_toolkit-3.0.53-py3-none-any.whl --output /work/wheels/prompt_toolkit-3.0.53-py3-none-any.whl \
    && echo '01c0891d7f9237d5e339f7d3e42cdae80b7534abb1c7c0e3352efba6231492f2  /work/wheels/prompt_toolkit-3.0.53-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b5/70/5d8df3b09e25bce090399cf48e452d25c935ab72dad19406c77f4e828045/psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl \
    && echo '076a2d2f923fd4821644f5ba89f059523da90dc9014e85f8e45a5774ca5bc6f9  /work/wheels/psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/22/a6/858897256d0deac81a172289110f31629fc4cee19b6f01283303e18c8db3/ptyprocess-0.7.0-py2.py3-none-any.whl --output /work/wheels/ptyprocess-0.7.0-py2.py3-none-any.whl \
    && echo '4b41f3967fce3af57cc7e94b888626c18bf37a083e3651ca8feeb66d492fef35  /work/wheels/ptyprocess-0.7.0-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/6d/18/83376915176eb058cb86470eb7396388a13350b09a8f233a79303bbcbc5b/pure_eval-0.2.4-py3-none-any.whl --output /work/wheels/pure_eval-0.2.4-py3-none-any.whl \
    && echo '96cae060a313cfaad51bb761278bfb0e62dc0248d9315a81173752dc546cd37a  /work/wheels/pure_eval-0.2.4-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/72/b8/b864503789ef5c58597d2a7b4adbee62c26440ab1e682581fc6838df8947/pydantic-2.14.3-py3-none-any.whl --output /work/wheels/pydantic-2.14.3-py3-none-any.whl \
    && echo '3f7b347782ab7e4cf4c798496ae3a82787d9f21ec12676a9c564355eeef8daa8  /work/wheels/pydantic-2.14.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/56/9c/621ad8f88590a92a086b1168dce09369d9c5e079e2e635e6646d248af55b/pydantic_core-2.50.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/pydantic_core-2.50.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo 'f1d62fb172db35c6478c9323da34ff37d1f3d37d7d44337a9d94ba8c583e5730  /work/wheels/pydantic_core-2.50.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/71/46/17f022dd3e953bf20a04a028a21ec746d942f8d2af30fa0f124fa0e6a684/pygments-2.21.0-py3-none-any.whl --output /work/wheels/pygments-2.21.0-py3-none-any.whl \
    && echo '2363c69b61c4a97c838da3b130dcd6468f4848992b21a82f2a63ec34377137d9  /work/wheels/pygments-2.21.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/2c/58/ca301544e1fa93ed4f80d724bf5b194f6e4b945841c5bfd555878eea9fcb/referencing-0.37.0-py3-none-any.whl --output /work/wheels/referencing-0.37.0-py3-none-any.whl \
    && echo '381329a9f99628c9069361716891d34ad94af76e461dcb0335825aecc7692231  /work/wheels/referencing-0.37.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a0/f4/c67b0b3f1b9245e8d266f0f112c500d50e5b4e83cb6f3b71b6528104182a/requests-2.34.2-py3-none-any.whl --output /work/wheels/requests-2.34.2-py3-none-any.whl \
    && echo '2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0  /work/wheels/requests-2.34.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/67/f3/6cd296376653270ac1b423bb30bd70942d9916b6978c6f40472d6ac038e7/retrying-1.4.2-py3-none-any.whl --output /work/wheels/retrying-1.4.2-py3-none-any.whl \
    && echo 'bbc004aeb542a74f3569aeddf42a2516efefcdaff90df0eb38fbfbf19f179f59  /work/wheels/retrying-1.4.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/22/9d/d08a1128ab199b2f0cf25bfeb0639bd05119fff4b7c47bec24ef9a8ec23f/rpds_py-2026.9.1-cp314-cp314-manylinux_2_17_x86_64.manylinux2014_x86_64.whl --output /work/wheels/rpds_py-2026.9.1-cp314-cp314-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
    && echo 'eac2f5dbafd585dfe31f86a23ebf0d3ba480a9d49ebc87947267b5608d4ea0cd  /work/wheels/rpds_py-2026.9.1-cp314-cp314-manylinux_2_17_x86_64.manylinux2014_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/ef/55/6dc6d6bb953bdfc52519a0059592c52b6e3b8ad51cf8256dffceb55b0610/setuptools-84.2.1-py3-none-any.whl --output /work/wheels/setuptools-84.2.1-py3-none-any.whl \
    && echo 'ca140b45d5325a9478f880e351484f62fef15f336462e449ca0c03c873d589c2  /work/wheels/setuptools-84.2.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f1/7b/ce1eafaf1a76852e2ec9b22edecf1daa58175c090266e9f6c64afcd81d91/stack_data-0.6.3-py3-none-any.whl --output /work/wheels/stack_data-0.6.3-py3-none-any.whl \
    && echo 'd5558e0c25a4cb0853cddad3d77da9891a08cb85dd9f9f91b9f8cd66e511e695  /work/wheels/stack_data-0.6.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/ad/66/0d785f0bc5e4315a96c989bb476d0fc07ea4f85132550c7b156ca2035d52/traitlets-5.16.1-py3-none-any.whl --output /work/wheels/traitlets-5.16.1-py3-none-any.whl \
    && echo 'f775618166caa0396c8e337099240f2bd3e5e917d203b2e6fbe21a58d3cb1f6b  /work/wheels/traitlets-5.16.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl --output /work/wheels/typing_extensions-4.16.0-py3-none-any.whl \
    && echo '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  /work/wheels/typing_extensions-4.16.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/de/0c/ea2544850a7c135e15033a5c7a8e7211136184b7ae63e2239d557c2b3019/typing_inspection-0.4.5-py3-none-any.whl --output /work/wheels/typing_inspection-0.4.5-py3-none-any.whl \
    && echo 'bc210535442b39e1bf2805e0c7a17dfd6a4ace760c84c7f7d16245d23a6b1c39  /work/wheels/typing_inspection-0.4.5-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/92/9d/c4e665119135114480843e7ab388fa94d8480650450e6f8e26b70d323a4c/urllib3-2.8.0-py3-none-any.whl --output /work/wheels/urllib3-2.8.0-py3-none-any.whl \
    && echo '0cf3cae568d36aa9576b28dfb35f11328f1cb974ca7647d9475ebb86c75ac6e3  /work/wheels/urllib3-2.8.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/6f/0c/309b1813b230d1dbbd6f2c2ab2bb21ef68992358977605d9ef289bbfedcc/wcwidth-0.9.4-py3-none-any.whl --output /work/wheels/wcwidth-0.9.4-py3-none-any.whl \
    && echo '901eace6d2dd25ebb917d0ce5db18e5c537e1504c905cf32f0d006c12098b05d  /work/wheels/wcwidth-0.9.4-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a1/38/df03f564f43cec2684823f3cccae1a652ee7face1cbaa76fb223096e64d7/werkzeug-3.1.9-py3-none-any.whl --output /work/wheels/werkzeug-3.1.9-py3-none-any.whl \
    && echo '6392e50c78460ba618e5b21f08a71f59c99ce99cdc6cf6e3dd7e6ccca8754fab  /work/wheels/werkzeug-3.1.9-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/34/95/40e17e20046b7bc820d29d09ae84ec157ec8dd6e6f6cd722626292c31b2e/widgetsnbextension-4.0.16-py3-none-any.whl --output /work/wheels/widgetsnbextension-4.0.16-py3-none-any.whl \
    && echo 'a31a8774885b96fe825462f5d6496166f0c7cae111195b6465c801d230eb5a4e  /work/wheels/widgetsnbextension-4.0.16-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b8/44/7bd2007260da11cccca29ba2d4c345f1287aa663db38ee7cefeabf6386a5/zipp-4.1.2-py3-none-any.whl --output /work/wheels/zipp-4.1.2-py3-none-any.whl \
    && echo 'b30cb6cd253122169c47de245ca24a86bac2a5d3802ba15bf7ba6414eb9e144d  /work/wheels/zipp-4.1.2-py3-none-any.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show open3d atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 libgl1 libegl1 libxkbcommon0 libfreetype6 libglib2.0-0 libfontconfig1 libx11-6 libxcb1 libxrender1 libxext6 libsm6 libice6 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
