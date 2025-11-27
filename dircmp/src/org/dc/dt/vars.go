package dt

import (
	"sync"
	"syscall"
)

var Dstats DStats
var Hits int
var Misses int
var Mu sync.Mutex
var Mu2 sync.Mutex
var Rmu sync.Mutex
var Rs RunStats
var Rts map[string]ST
var Wg sync.WaitGroup

const (
	Unknown EType = iota
	File
	Dir
)

var ETName = []string{
	"Unknown",
	"File",
	"Dir",
}

var (
	kernel32, _             = syscall.LoadLibrary("kernel32.dll")
	getVolumeInformation, _ = syscall.GetProcAddress(kernel32, "GetVolumeInformationW")
	copyFile, _             = syscall.GetProcAddress(kernel32, "CopyFileW")
)

const (
	noOp OpCode = iota
	DCrt
	DMis
	FMis
	FNew
	FExi
	DNew
	DExi
	DDel
)

var OpCodes = []string{
	"noOp",
	"DCrt",
	"DMis",
	"FMis",
	"FNew",
	"FExi",
	"DNew",
	"DExi",
	"DDel",
}

