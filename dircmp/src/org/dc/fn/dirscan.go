package fn

import (
	"regexp"

	"log"

	"org/dc/dt"
)

func Find(d *dt.DItem, re string) (fpl []dt.DItem) {
	fpl = []dt.DItem{}
	var c = d.GetContents()
	var di = dt.DI{d, c}
	scanDir(di, re, &fpl)
	return fpl
}

var cre *regexp.Regexp

func scanDir(di dt.DI, re string, fpl *[]dt.DItem) {
	if cre == nil {
		var err error
		cre, err = regexp.Compile(re)
		if err != nil {
			log.Println(err.Error())
			return
		}
	}
	if !di.C.Blocked {
		var nsi dt.DItem
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
			scanDir(dt.DI{&nsi, nsi.DirContents()}, re, fpl)
		}
	}
}
