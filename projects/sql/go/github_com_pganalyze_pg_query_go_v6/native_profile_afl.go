//go:build afl

package sqlharness

// FlushNativeCoverage is a no-op in the AFL++ build, which has no Clang profile runtime.
func FlushNativeCoverage() int { return 0 }
