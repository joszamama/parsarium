package main

/*
int __llvm_profile_write_file(void);
*/
import "C"

func writeNativeProfile() int { return int(C.__llvm_profile_write_file()) }
