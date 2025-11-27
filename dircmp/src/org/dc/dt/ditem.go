package dt

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"time"
)

func (d *DItem) GetContents() *Contents {
	Misses++
	return d.DirContents()
}

func (d *DItem) blocked() bool {
	var b1 = func() bool { return strings.Contains(d.Fp(), "$RECYCLE.BIN") }
	var b2 = func() bool { return strings.Contains(d.Fp(), "System Volume Information") }
	return b1() || b2()
}

func (d *DItem) DirContents() (c *Contents) {
	Mu.Lock()
	defer Mu.Unlock()
	c = &Contents{
		make(map[string]DE),
		make(map[string]DE),
		false,
		d.blocked(),
		time.Now().UnixNano(), 0, 0,
	}
	var des, err = ioutil.ReadDir(d.Fp())
	if err == nil {
		c.Dex = true
		for _, it := range des {
			var de1 = FromFI(it)
			if de1.EType == Dir {
				c.Dirs[de1.Fname] = *de1
			} else if de1.EType == File {
				c.Files[de1.Fname] = *de1
			}
		}
	} else {
		switch perr := err.(type) {
		case *os.PathError:
			switch perr.Err {
				case os.ErrInvalid:
					c.Blocked = true
				case os.ErrPermission:
					c.Blocked = true
				case os.ErrNotExist:
					c.Dex = false
				case os.ErrExist:
				case os.ErrClosed:
			}
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
