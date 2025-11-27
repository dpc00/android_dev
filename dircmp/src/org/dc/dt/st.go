package dt

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

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
	var v1 = st.Pth[1:]
	return string(os.PathSeparator) + filepath.Join(v1...)
}

func (st *ST) SDir(rd string) *DItem {
	return &DItem{Dir, *st, rd, nil, nil}
}

func (st *ST) SFile(fn string) *DItem {
	return &DItem{File, *st, fn, nil, nil}
}

func (st *ST) String() string {
	return fmt.Sprintf("%s (%s) %s", st.Vl, st.Pth[0], st.Rp())
}
