# iio/libmergepdf — PDF / PHP

Pinned release: `4.0.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/pdf/php/iio-libmergepdf/README.md)

## Run from the repository root

```sh
python3 parsarium.py build pdf php iio_libmergepdf
python3 parsarium.py run pdf php iio_libmergepdf controls/pdf/one-page.pdf
python3 parsarium.py replay pdf php iio_libmergepdf CORPUS_DIR runs/pdf-iio_libmergepdf-replay
python3 parsarium.py afl build pdf php iio_libmergepdf
python3 parsarium.py afl prepare pdf php iio_libmergepdf runs/pdf-iio_libmergepdf-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
