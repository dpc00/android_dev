package fn

import (
	"regexp"

	. "../dt"
	. "log"
)

type DI struct {
	D *DItem
	C *Contents
}

func Find(d *DItem, re string) (fpl []DItem) {
	fpl = []DItem{}
	var c = d.GetContents()
	var di = DI{d, c}
	scanDir(di, re, &fpl)
	return fpl
}

var cre *regexp.Regexp

func scanDir(di DI, re string, fpl *[]DItem) {
	if cre == nil {
		var err error
		cre, err = regexp.Compile(re)
		if err != nil {
			Println(err.Error())
			return
		}
	}
	if !di.C.Blocked {
		var nsi DItem
		for _, de := range di.C.Files {
			var fn = de.Fname
			nsi = *di.D.SubFile(fn)
			matched := cre.MatchString(nsi.Fp())
			if matched {
				*fpl = append(*fpl, nsi)
			}
		}
		for _, de := range di.C.Dirs {
			var fn = de.Fname
			nsi = *di.D.SubDir(fn)
			matched, err := regexp.MatchString(re, nsi.Fp())
			if err == nil && matched {
				*fpl = append(*fpl, nsi)
			}
			scanDir(DI{&nsi, nsi.GetContents()}, re, fpl)
		}
	}
}
