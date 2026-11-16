# imagine/imagine — PNG / PHP

Pinned release: `1.5.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/imagine-imagine/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php imagine_imagine
python3 parsarium.py run png php imagine_imagine controls/png/red-green.png
python3 parsarium.py replay png php imagine_imagine CORPUS_DIR runs/png-imagine_imagine-replay
python3 parsarium.py afl build png php imagine_imagine
python3 parsarium.py afl prepare png php imagine_imagine runs/png-imagine_imagine-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
