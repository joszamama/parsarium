#!/bin/sh
# Run inside the pinned golang image (see README.md). Parses each untagged Go
# plain-MP3 control twice and lists the covered mattetti/audio/mp3 Go cover blocks,
# the same block features the Go AFL++ bridge maps to tuples.
set -eu
PKG=github.com/mattetti/audio/mp3
cp -r /probe /tmp/probe
cd /tmp/probe
go mod download
echo "ad0c168c6db73a17d8891adefce9340142015318491536853713890f0056dafb  $(go env GOMODCACHE)/cache/download/github.com/mattetti/audio/@v/v0.0.0-20240411020228-c5379f9b5b61.zip" | sha256sum --check >&2
CGO_ENABLED=0 go test -c -coverpkg=$PKG -o probe.test .
for control in go-tone-44k-mono go-tone-22k-stereo; do
  for repeat in 1 2; do
    PROBE_INPUT=/controls/$control.mp3 ./probe.test -test.run=TestProbe \
      -test.coverprofile=$control.$repeat.cov > $control.$repeat.out
    grep '^OBSERVED_JSON:' $control.$repeat.out | sed "s/^OBSERVED_JSON:/$control $repeat /"
    awk -v p="$PKG/" 'NR>1 && index($1,p)==1 && $3>0 {print $1}' $control.$repeat.cov | sort -u > $control.$repeat.blocks
  done
  cmp $control.1.blocks $control.2.blocks
  echo "$control blocks $(wc -l < $control.1.blocks)"
done
echo "difference $(comm -3 go-tone-44k-mono.1.blocks go-tone-22k-stereo.1.blocks | wc -l)"
go version
