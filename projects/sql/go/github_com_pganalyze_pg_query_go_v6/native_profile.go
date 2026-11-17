//go:build !afl

package sqlharness

/*
int __llvm_profile_write_file(void);
*/
import "C"

// FlushNativeCoverage writes the Clang profile of the bundled libpg_query C sources;
// Go exits without running C atexit handlers.
func FlushNativeCoverage() int { return int(C.__llvm_profile_write_file()) }
