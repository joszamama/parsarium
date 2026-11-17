//go:build !afl

package vipsgenpnm

/*
int __llvm_profile_write_file(void);
*/
import "C"

func FlushNativeCoverage() int { return int(C.__llvm_profile_write_file()) }
