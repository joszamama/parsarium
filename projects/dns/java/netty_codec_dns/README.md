# netty-codec-dns — DNS / Java

Pinned release: `4.2.21.Final`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/java/netty-codec-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns java netty_codec_dns
python3 parsarium.py run dns java netty_codec_dns controls/dns/response.bin
python3 parsarium.py replay dns java netty_codec_dns CORPUS_DIR runs/dns-netty_codec_dns-replay
python3 parsarium.py afl build dns java netty_codec_dns
python3 parsarium.py afl prepare dns java netty_codec_dns runs/dns-netty_codec_dns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
