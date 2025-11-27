package dt

import (
	. "fmt"
	"strings"
)

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

func (s *Stats) String() string {
	var s1 = "dir"
	var s2 = "file"
	var s3 = "byte"
	if s.Dirs != 1 {
		s1 += "s"
	}
	if s.Files != 1 {
		s2 += "s"
	}
	if s.Bytes != 1 {
		s3 += "s"
	}
	return Sprintf("%s, %s, %s", FmtInt(s.Dirs, s1), FmtInt(s.Files, s2), FmtInt2(s.Bytes, s3))
}

func (s *Copied) String() string {
	return Sprintf("copied %s", s.Stats.String())
}

func (s *Deleted) String() string {
	return Sprintf("deleted %s", s.Stats.String())
}

func (s *Scanned) String() string {
	return Sprintf("scanned %s", s.Stats.String())
}

func (ds *DStats) String() string {
	return Sprintf("%s\n", ds.Deleted.String()) +
		Sprintf("%s\n", ds.Copied.String()) +
		Sprintf("%s\n", ds.Scanned.String()) +
		Sprintf("%d errors/failures.\n", ds.Errors)
}

func LogPrintlns(s string) {
	var sa = strings.Split(s, "\n")
	for _, s2 := range sa {
		Printf("%s\n", s2)
	}
}

func PrintStats() {
	LogPrintlns(Dstats.String())
}

var Dstats DStats
