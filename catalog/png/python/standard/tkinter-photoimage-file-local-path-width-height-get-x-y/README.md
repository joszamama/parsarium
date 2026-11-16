# tkinter.PhotoImage(file=local path); width(); height(); get(x, y) — PNG / Python

- **Runtime:** CPython 3.13.1 with bundled Tk 8.6
- **Input API:** `tkinter.PhotoImage(file=local path); width(); height(); get(x, y)`
- **Official documentation:** [reference](https://docs.python.org/3.13/library/tkinter.html#images)
- **Valid control:** [`controls/png/red-green.png`](../../../../../controls/png/red-green.png)
- **Inventory and verification:** [standard API record](../../../../../data/python/png/standard.json) · [saved result](../../../../../data/python/png/verification.json)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgb0": [
    255,
    0,
    0
  ],
  "rgb1": [
    0,
    255,
    0
  ]
}
```

[Control adapter](../../../../../adapters/python/png/standard.py)

## Run this control

[Docker harness and control receipt](../../../../../projects/png/python/stdlib_tkinter_photoimage/README.md)

```sh
python3 projects/png/python/stdlib_tkinter_photoimage/verify-control.py
```

Tk's native PNG reader has measured source coverage on this control. AFL++ parser feedback is unavailable, so this path remains staged.
