# fgergo/mp3: byte-identical fork of tcolgate/mp3

`github.com/fgergo/mp3` v1.0.0 (MIT, module ZIP SHA-256 `e9c3f74daffc42e511d00cbd2ea6f67e08fa16f6d54e714dcb9ed12cdbc92781`, Go module sum `h1:TmAZJhUW2k/t1Azu3HOPCBMSKqg3gxP7WLkOFi92L7k=`) has **2 Imported by** packages in the [saved pkg.go.dev snapshot](../../registry-snapshot.json). Its package documentation and API are the same as the selected `github.com/tcolgate/mp3` (62 Imported by).

The module was compared file by file with the pinned `tcolgate/mp3` release `v0.0.0-20170426193717-e79c5a46d300` (ZIP SHA-256 `20f833eba102520fc4efd0c473fa3591bb098df25422f5b16e802bfcf9f8e16d`). Of the 16 files in that release, 15 are byte-identical in the fork, including every parser source file. `silence.go` differs only in the import path of its `internal/data` package. The fork adds a `go.mod` with `module github.com/fgergo/mp3` and `go 1.14`. [result.json](result.json) lists the hashes.

Because the parser code is the same, a Docker harness would repeat the `tcolgate/mp3` receipt under a different module path. The path is recorded as a shared-family duplicate and is not counted separately. No control, coverage or AFL++ claim is made for it.
