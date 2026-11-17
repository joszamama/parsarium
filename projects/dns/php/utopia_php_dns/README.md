# utopia-php/dns — DNS / PHP

Pinned release: `3.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/php/utopia-php-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns php utopia_php_dns
python3 parsarium.py run dns php utopia_php_dns controls/dns/response.bin
python3 parsarium.py replay dns php utopia_php_dns CORPUS_DIR runs/dns-utopia_php_dns-replay
python3 parsarium.py afl build dns php utopia_php_dns
python3 parsarium.py afl prepare dns php utopia_php_dns runs/dns-utopia_php_dns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
