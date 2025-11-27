package dt

import (
	"fmt"
)

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
	return fmt.Sprintf("%s, %s, %s", FmtInt(s.Dirs, s1), FmtInt(s.Files, s2), FmtInt2(s.Bytes, s3))
}

func (s *Copied) String() string {
	return fmt.Sprintf("copied %s", s.Stats.String())
}

func (s *Deleted) String() string {
	return fmt.Sprintf("deleted %s", s.Stats.String())
}

func (s *Scanned) String() string {
	return fmt.Sprintf("scanned %s", s.Stats.String())
}

func (ds *DStats) String() string {
	return fmt.Sprintf("%s\n", ds.Deleted.String()) +
		fmt.Sprintf("%s\n", ds.Copied.String()) +
		fmt.Sprintf("%s\n", ds.Scanned.String()) +
		fmt.Sprintf("%d errors/failures.\n", ds.Errors)
}
