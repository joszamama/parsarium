FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# mitmproxy 12.3.1 (py3-none-any wheel) and its runtime requirements as manylinux/py3 wheels, all pinned by hash
# (mitmproxy_macos is a darwin-only requirement of mitmproxy_rs and is not installed).
RUN mkdir /work/wheels /work/mitmproxy-wheel && cd /work/wheels \
    && for url in \
       https://files.pythonhosted.org/packages/b0/0f/4a280923313b831892caaa45348abea89e7dd2e4422a86699bb0e506b1dd/aioquic-1.2.0-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
       https://files.pythonhosted.org/packages/4f/d3/a8b22fa575b297cd6e3e3b0155c7e25db170edf1c74783d6a31a2490b8d9/argon2_cffi-25.1.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/7a/82/a9226c27133c26c7892ebc7b174304f81774a78c5b1e97a96e3c15b2cba8/argon2_cffi_bindings-26.2.0-cp310-abi3-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl \
       https://files.pythonhosted.org/packages/c0/1b/54f4ad77cd8a584fa70746c47df988e002cf1ee1eba43364d46f87803647/asgiref-3.12.1-py3-none-any.whl \
       https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
       https://files.pythonhosted.org/packages/64/b4/17d4b0b2a2dc85a6df63d1157e028ed19f90d4cd97c36717afef2bc2f395/attrs-26.1.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/e4/6e/b77ade812672d15cf50842e167eead80ac3514f3beacac8902915417f8b7/bcrypt-5.0.0-cp39-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
       https://files.pythonhosted.org/packages/10/cb/f2ad4230dc2eb1a74edf38f1a38b9b52277f75bef262d8908e60d957e13c/blinker-1.9.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/c4/07/8948582ce173e8e43cea9fadb8c3c3ea94800fb9814119c9239c1ae6c797/brotli-1.2.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
       https://files.pythonhosted.org/packages/32/d1/a3652fe2c19134d0d15922177821d863cbd7e842d53a21bbe7e8e3a1b5ac/certifi-2026.10.23-py3-none-any.whl \
       https://files.pythonhosted.org/packages/e9/02/4e7d553a7ac4b4238b38b3c1b80d486e9d4436f8d2acbf87a0997fe3f402/cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
       https://files.pythonhosted.org/packages/31/7d/164b7ffc8624fe9efb4221bf9af485d5c1e41b9ae118045d2b6dc5457d8b/click-8.5.1-py3-none-any.whl \
       https://files.pythonhosted.org/packages/21/69/64cef1f702bf6657e0cc186ed1a2891d50d29fb41586b254e1c07adea261/cryptography-50.0.2-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
       https://files.pythonhosted.org/packages/7f/9c/34f6962f9b9e9c71f6e5ed806e0d0ff03c9d1b0b2340088a0cf4bce09b18/flask-3.1.3-py3-none-any.whl \
       https://files.pythonhosted.org/packages/04/4b/29cac41a4d98d144bf5f6d33995617b185d14b22401f75ca86f384e87ff1/h11-0.16.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/7e/22/e85faf23bd72a92d1921e37d674ca56eb298a3c8be31fdecef0ff2b3aaac/h2-4.4.1-py3-none-any.whl \
       https://files.pythonhosted.org/packages/71/b4/4a9fcfb2aef6ba44d9073ecd301443aa00b3dac95de5619f2a7de7ec8a91/hpack-4.2.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/48/30/47d0bf6072f7252e6521f3447ccfa40b421b6824517f82854703d0f5a98b/hyperframe-6.1.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/04/96/92447566d16df59b2a776c0fb82dbc4d9e07cd95062562af01e408583fc4/itsdangerous-2.2.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/62/a1/3d680cbfd5f4b8f15abc1d571870c5fc3e594bb582bc3b64ea099db13e56/jinja2-3.1.6-py3-none-any.whl \
       https://files.pythonhosted.org/packages/4a/4a/cf14bf3b1f5ffb13c69cf5f0ea78031247790558ee88984a8bdd22fae60d/kaitaistruct-0.11-py2.py3-none-any.whl \
       https://files.pythonhosted.org/packages/4e/f6/71d6ec9f18da0b2201287ce9db6afb1a1f637dedb3f0703409558981c723/ldap3-2.9.1-py2.py3-none-any.whl \
       https://files.pythonhosted.org/packages/8f/db/d7282caf7ab03af44d5d6fdbaa019b35c7d7f1c90588b839c07cba640d6a/markupsafe-3.0.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl \
       https://files.pythonhosted.org/packages/a7/b2/886992a28a7bf86e47691d7a33e26eba370ee71d89b77d3128412910a33e/mitmproxy-12.3.1-py3-none-any.whl \
       https://files.pythonhosted.org/packages/f2/b2/90837d64dec0aad3483edb0977d4792acf111047415c9dc4e5ed008fc7ff/mitmproxy_linux-0.12.16-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
       https://files.pythonhosted.org/packages/89/d4/f2f638b4ed4d5f585b2dfcf445d31fed95f0b2d0f79106af49a20656995b/mitmproxy_rs-0.12.16-cp312-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
       https://files.pythonhosted.org/packages/9d/16/053c2945c5e3aebeefb4ccd5c5e7639e38bc30ad1bdc7ce86c6d01707726/publicsuffix2-2.20191221-py2.py3-none-any.whl \
       https://files.pythonhosted.org/packages/19/1f/3eefd5c84c35cae44549ce1c7f7e58f7945b34f5a6bce07a135438522073/pyasn1-0.6.5-py3-none-any.whl \
       https://files.pythonhosted.org/packages/b6/ae/315bbeee126a769cbde43cf4908acb4b40408d8bf8bbf334dd7368d8dadf/pycparser-3.12-py3-none-any.whl \
       https://files.pythonhosted.org/packages/22/5b/06f5e354ed882ce036ed65f2a393c98d0f6c71a23fa64b53251ddeb40a7b/pylsqpack-0.3.24-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl \
       https://files.pythonhosted.org/packages/51/ad/2cf6d3fa2fae5c79e1ed9960c0d42badd0f94d81dd12b50604cdc839e648/pyopenssl-26.4.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/38/bb/d215ee7c73b61497b28a5503f9f53523f294fcc936762b7caf90e0c1c2b5/pyparsing-3.3.3-py3-none-any.whl \
       https://files.pythonhosted.org/packages/df/80/fc9d01d5ed37ba4c42ca2b55b4339ae6e200b456be3a1aaddf4a9fa99b8c/pyperclip-1.11.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/b8/0c/51f6841f1d84f404f92463fc2b1ba0da357ca1e3db6b7fbda26956c3b82a/ruamel_yaml-0.19.1-py3-none-any.whl \
       https://files.pythonhosted.org/packages/93/eb/2433e1af4ff903499144de4846569fb3300b816179ae99a03c2f011b666a/service_identity-26.1.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/32/46/9cb0e58b2deb7f82b84065f37f3bffeb12413f947f9388e4cac22c4621ce/sortedcontainers-2.4.0-py2.py3-none-any.whl \
       https://files.pythonhosted.org/packages/60/33/df6d7d04854a58619f8349a51e3edb138324130a7562b0bb21f115bb940f/tornado-6.5.10-cp39-abi3-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl \
       https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl \
       https://files.pythonhosted.org/packages/0a/e9/4a31e301daab899c550767e417c7e4b1a4773591d3298d59db0393034a1b/urwid-4.0.13-py3-none-any.whl \
       https://files.pythonhosted.org/packages/fa/e8/0485850748dfdba9443f4151c7b2442cfa4987ba6cd871038eb5d6b8eca9/wcwidth-0.9.4-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
       https://files.pythonhosted.org/packages/a1/38/df03f564f43cec2684823f3cccae1a652ee7face1cbaa76fb223096e64d7/werkzeug-3.1.9-py3-none-any.whl \
       https://files.pythonhosted.org/packages/a4/f5/10b68b7b1544245097b2a1b8238f66f2fc6dcaeb24ba5d917f52bd2eed4f/wsproto-1.3.2-py3-none-any.whl; \
       do curl --fail --location --retry 3 -O "$url" || exit 1; done \
    && printf '%s\n' \
       '43ae3b11d43400a620ca0b4b4885d12b76a599c2cbddba755f74bebfa65fe587  aioquic-1.2.0-cp38-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl' \
       'fdc8b074db390fccb6eb4a3604ae7231f219aa669a2652e0f20e16ba513d5741  argon2_cffi-25.1.0-py3-none-any.whl' \
       '2d475baecbcb506e40ab1cb05a84c9cc913a8950061a4045fd0ec0eb54aa7fa2  argon2_cffi_bindings-26.2.0-cp310-abi3-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl' \
       'fe386d1c2bff7259ea95929266d12a8cf9a8b5a1c2598402967d8792e7a7c094  asgiref-3.12.1-py3-none-any.whl' \
       '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' \
       'c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309  attrs-26.1.0-py3-none-any.whl' \
       '7aeef54b60ceddb6f30ee3db090351ecf0d40ec6e2abf41430997407a46d2254  bcrypt-5.0.0-cp39-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' \
       'ba0efaa9080b619ff2f3459d1d500c57bddea4a6b424b60a91141db6fd2f08bc  blinker-1.9.0-py3-none-any.whl' \
       'a998857af4fcd19920bdf5f30f0f1a23f38472a703d33e49168cd4fd32438377  brotli-1.2.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' \
       'e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1  certifi-2026.10.23-py3-none-any.whl' \
       'b0431303acaea1089ad4b3e9ce4e6518193def1118d4073ca848635ee4ea2e96  cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' \
       '8bb5376d2006950386f8c6427613334a2acadc5f559cb80e638d00b4df957e37  click-8.5.1-py3-none-any.whl' \
       '630ebfea3bf689d075f82316324ff7433dc447fe6bc1bfc76524b74b4a9567d2  cryptography-50.0.2-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' \
       'f4bcbefc124291925f1a26446da31a5178f9483862233b23c0c96a20701f670c  flask-3.1.3-py3-none-any.whl' \
       '63cf8bbe7522de3bf65932fda1d9c2772064ffb3dae62d55932da54b31cb6c86  h11-0.16.0-py3-none-any.whl' \
       '0e25f1462b23c9cb82d9eb02e28bc706dac2a68cb457c6a0d74d63c8a2a5d0e6  h2-4.4.1-py3-none-any.whl' \
       '858ac0b02280fa582b5080d68db0899c62a80375e0e5413a74970c5e518b6986  hpack-4.2.0-py3-none-any.whl' \
       'b03380493a519fce58ea5af42e4a42317bf9bd425596f7a0835ffce80f1a42e5  hyperframe-6.1.0-py3-none-any.whl' \
       'c6242fc49e35958c8b15141343aa660db5fc54d4f13a1db01a3f5891b98700ef  itsdangerous-2.2.0-py3-none-any.whl' \
       '85ece4451f492d0c13c5dd7c13a64681a86afae63a5f347908daf103ce6d2f67  jinja2-3.1.6-py3-none-any.whl' \
       '5c6ce79177b4e193a577ecd359e26516d1d6d000a0bffd6e1010f2a46a62a561  kaitaistruct-0.11-py2.py3-none-any.whl' \
       '5869596fc4948797020d3f03b7939da938778a0f9e2009f7a072ccf92b8e8d70  ldap3-2.9.1-py2.py3-none-any.whl' \
       'a8e9f292fcda89b324f2f5c91d13f1424a153e40fc2756f38ee23b15835ff300  markupsafe-3.0.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl' \
       '87afb808ac8d55383dbe6aa30eadeb0fedaeffd26210e7e23c25c9cd43bdb36a  mitmproxy-12.3.1-py3-none-any.whl' \
       '87409215261b56ea7ccfedb0fe37b0f4accdd5e84d32596f6bdbabd0f42e5a9f  mitmproxy_linux-0.12.16-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' \
       'f790729a26e26f3af2542f5a7e274cec757369098b95a25788600e6d1d12166f  mitmproxy_rs-0.12.16-cp312-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' \
       '786b5e36205b88758bd3518725ec8cfe7a8173f5269354641f581c6b80a99893  publicsuffix2-2.20191221-py2.py3-none-any.whl' \
       '4017b0fce125096b8573b39c989fdb1a4b19cf761e683398184550fea0e66587  pyasn1-0.6.5-py3-none-any.whl' \
       'a076f3f489b39b43ed13563a1dafe42447445bec2e294154ec5c57fcdda4c85e  pycparser-3.12-py3-none-any.whl' \
       '6024854eb16d32803d4890fb90a73b9348c74b61c0770680aefaaa75f8456e8c  pylsqpack-0.3.24-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl' \
       'f0eb0cb2d581d3ad2b9c489468485e7f2ab6727d08401bcf9d824c3caddf3c1c  pyopenssl-26.4.0-py3-none-any.whl' \
       'ece8c00a69cf01b45d0b1dedabb469c90d8caf996d4fda40f147627a122849a4  pyparsing-3.3.3-py3-none-any.whl' \
       '299403e9ff44581cb9ba2ffeed69c7aa96a008622ad0c46cb575ca75b5b84273  pyperclip-1.11.0-py3-none-any.whl' \
       '27592957fedf6e0b62f281e96effd28043345e0e66001f97683aa9a40c667c93  ruamel_yaml-0.19.1-py3-none-any.whl' \
       '68c32dadbb69135fb951077677e07cd7f6031020f3a8c8f47a28cda8a0742118  service_identity-26.1.0-py3-none-any.whl' \
       'a163dcaede0f1c021485e957a39245190e74249897e2ae4b2aa38595db237ee0  sortedcontainers-2.4.0-py2.py3-none-any.whl' \
       'bdf942448169e5336451d0494d7e3d81cfa726d5aa312affdc4682dd62a62f6d  tornado-6.5.10-cp39-abi3-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl' \
       '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  typing_extensions-4.16.0-py3-none-any.whl' \
       'bee62404d24d06d9ffa74d834b03d5ba53c419a135b36831775fc69c6246e6fa  urwid-4.0.13-py3-none-any.whl' \
       'b185c8b927b23af2721be1783499d1cfa5c028b098b0858951b4ae224477f1c2  wcwidth-0.9.4-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' \
       '6392e50c78460ba618e5b21f08a71f59c99ce99cdc6cf6e3dd7e6ccca8754fab  werkzeug-3.1.9-py3-none-any.whl' \
       '61eea322cdf56e8cc904bd3ad7573359a242ba65688716b0710a5eb12beab584  wsproto-1.3.2-py3-none-any.whl' \
       | sha256sum --check \
    && unzip -q /work/wheels/mitmproxy-12.3.1-py3-none-any.whl -d /work/mitmproxy-wheel \
    && grep -Fx 'Classifier: License :: OSI Approved :: MIT License' /work/mitmproxy-wheel/mitmproxy-12.3.1.dist-info/METADATA \
    && cd /work/mitmproxy-wheel \
    && printf '%s\n' \
       '88f137c0e5b838e4e18fefc9bdb30b46e0956b6889e050c7646c5c488ead8904  mitmproxy/dns.py' \
       '5dd691893c86d41771599b25de9e7ddb84bd9871f1925832775ce73e54d2f87a  mitmproxy/net/dns/domain_names.py' \
       'cc4ab04ed7180af6c0ede7147f9ec2aa05212c088d7b3c8e38bbffe91c9c8f82  mitmproxy-12.3.1.dist-info/LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/mitmproxy-wheel/mitmproxy/net/dns /opt/venv/lib/python3.14/site-packages/mitmproxy/net/dns \
    && cmp /work/mitmproxy-wheel/mitmproxy/dns.py /opt/venv/lib/python3.14/site-packages/mitmproxy/dns.py \
    && /opt/venv/bin/python -c 'import mitmproxy.dns, importlib.metadata as m; assert m.version("mitmproxy") == "12.3.1"' \
    && { python3 --version; /opt/venv/bin/pip show mitmproxy mitmproxy_rs atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum mitmproxy/dns.py mitmproxy/net/dns/domain_names.py; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py replay.py run-control.py /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
