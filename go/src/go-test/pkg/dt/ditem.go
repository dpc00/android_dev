package dt

import (
	"fmt"
	"path/filepath"
	"strings"
	"time"
)

type DItem struct {
	EType
	ST
	Rd string
	fp *string
	rp *string
}

type DISlice []DItem

func (p DISlice) Len() int           { return len(p) }
func (p DISlice) Less(i, j int) bool { return p[i].Fp() < p[j].Fp() }
func (p DISlice) Swap(i, j int)      { p[i], p[j] = p[j], p[i] }

var Hits int
var Misses int

func (d *DItem) GetContents() *Contents {
	Misses++
	return d.ContentsOf()
}

func (d *DItem) blocked() bool {
	var b1 = func() bool { return strings.Contains(d.Fp(), "$RECYCLE.BIN") }
	var b2 = func() bool { return strings.Contains(d.Fp(), "System Volume Information") }
	var b3 = func() bool { return strings.Contains(d.Fp(), "PortableApps\\FirefoxPortable\\Data\\profile") }
	return b1() || b2() || b3()
}

func (d *DItem) String() string {
	return fmt.Sprintf("%s [%s]", d.ST.String(), d.Rd)
}

func (d *DItem) GetVl() string {
	return d.ST.GetVl()
}

func (d *DItem) Fp() string {
	if d.fp == nil {
		var v1 string = filepath.Join(d.ST.Fp(), d.Rd)
		d.fp = &v1
	}
	return *d.fp
}

func (d *DItem) Rp() string {
	if d.rp == nil {
		var v1 string = filepath.Join(d.ST.Rp(), d.Rd)
		d.rp = &v1
	}
	return *d.rp
}

func (d *DItem) SubDir(rd string) *DItem {
	return &DItem{Dir, d.ST, filepath.Join(d.Rd, rd), nil, nil}
}

func (d *DItem) SubFile(rd string) *DItem {
	return &DItem{File, d.ST, filepath.Join(d.Rd, rd), nil, nil}
}

func (d *DItem) Parent() *DItem {
	return &DItem{Dir, d.ST, filepath.Dir(d.Rd), nil, nil}
}

func (d *DItem) ContentsOf() (c *Contents) {
	c = &Contents{
		make(map[string]DE),
		make(map[string]DE),
		false,
		d.blocked(),
		time.Now().UnixNano(), 0, 0,
	}
	var des, err = ReadDir(d.Fp())
	if err == nil {
		c.Dex = true
		for _, it := range des {
			var de1 = it
			if de1.EType == Dir {
				c.Dirs[de1.Fname] = *de1
			} else if de1.EType == File {
				c.Files[de1.Fname] = *de1
			}
		}
	} else {
		switch(err.Error()) {
		case "Access is denied.":
			c.Dex = true
			c.Blocked = true
		case "The system cannot find the file specified.", "The system cannot find the path specified.", "The directory name is invalid.":
			c.Dex = false
			c.Blocked = false
		default:
			fmt.Printf("err.Error() %s\n", err.Error())
		}
	}
	Rmu.Lock()
	Dstats.Scanned.Dirs += 1
	Dstats.Scanned.Files += len(c.Files)
	for _, de := range c.Files {
		Dstats.Scanned.Bytes += de.Size
	}
	Rmu.Unlock()
	return
}
