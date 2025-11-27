package dt

import "time"

type EType uint8
type OpCode uint8

type Contents struct {
	Files   map[string]DE
	Dirs    map[string]DE
	Dex     bool
	Blocked bool
	Ftime   int64
	Utime   int64
	LCtime  int64
}

type Stats struct {
	Bytes int64
	Files int
	Dirs  int
}

type Copied struct {
	Stats
}

type Deleted struct {
	Stats
}

type Scanned struct {
	Stats
}

type DStats struct {
	Deleted Deleted
	Copied  Copied
	Scanned Scanned
	Errors  int
}

type RunStats struct {
	Recno int
	T1    int64
	T2    int64
	T3    int64
	S     DStats
}

type DI struct {
	D *DItem
	C *Contents
}

type ST struct {
	Vl  string
	Pth []string
}

type DItem struct {
	EType
	ST
	Rd string
	fp *string
	rp *string
}



type DE struct {
	EType
	Fname string
	Mtime time.Time
	Size  int64
}

type OpList map[OpCode][]DE

type DISlice []DItem
