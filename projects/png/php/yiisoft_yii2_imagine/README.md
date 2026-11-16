# yiisoft/yii2-imagine — PNG / PHP

Pinned release: `2.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/png/php/yiisoft-yii2-imagine/README.md)

## Run from the repository root

```sh
python3 parsarium.py build png php yiisoft_yii2_imagine
python3 parsarium.py run png php yiisoft_yii2_imagine controls/png/red-green.png
python3 parsarium.py replay png php yiisoft_yii2_imagine CORPUS_DIR runs/png-yiisoft_yii2_imagine-replay
python3 parsarium.py afl build png php yiisoft_yii2_imagine
python3 parsarium.py afl prepare png php yiisoft_yii2_imagine runs/png-yiisoft_yii2_imagine-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
