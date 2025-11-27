package dt

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	. "sync"
)

type ST struct {
	Vl  string
	Pth []string
	Q   []string
	Sf  func()
	Wg  WaitGroup
}

func (st *ST) String() string {
	return fmt.Sprintf("%s (%s) %s %s %v %v", st.Vl, st.Pth[0], st.Rp(), st.Q, st.Sf, st.Wg)
}

func (dst *ST) Run(src *ST, sF func(*ST, *ST, string) []error) {
	dst.Wg.Add(1)
	dst.Sf = func() {
		for len(dst.Q) > 0 {
			var crd = (dst.Q)[0]
			dst.Q = append([]string{}, dst.Q[1:]...)
			errs := sF(src, dst, crd)
			if len(errs) > 0 {
				fmt.Printf("%v\n", errs)
			}
		}
		dst.Sf = nil
		dst.Wg.Done()
	}
	go dst.Sf()
}

func (st *ST) GetVl() string {
	return st.Vl
}

func (st *ST) Fp() string {
	var rv string
	if len(st.Pth) == 1 {
		rv = st.Pth[0] + string(os.PathSeparator)
	} else {
		rv = st.Pth[0] + string(os.PathSeparator) + strings.Join(st.Pth[1:], string(os.PathSeparator))
	}
	return rv
}

func (st *ST) Rp() string {
	var rp1 = st.Pth[1:]
	return string(os.PathSeparator) + filepath.Join(rp1...)
}

func (st *ST) SDir(rd string) *DItem {
	return &DItem{Dir, *st, rd, nil, nil}
}

func (st *ST) SFile(fn string) *DItem {
	return &DItem{File, *st, fn, nil, nil}
}
