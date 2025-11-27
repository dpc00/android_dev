package fn

import (
	. "../../pkg/dt"
	"errors"
	. "fmt"
	"os"
	"path/filepath"
)

func delDir(dd *DItem) error {
	var err = os.RemoveAll(dd.Fp())
	return err
}

func SyncTree(src, dst *ST, rd string) (errs []error) {
	var sd = src.SDir(rd)
	var dd = dst.SDir(rd)
	var sc = sd.GetContents()
	var dc = dd.GetContents()

	var ol = MakeOpList(sc, dc)

	errs = []error{}

	var justDExi = func(ol OpList) bool {
		for k := range ol {
			if k != DExi {
				return false
			}
		}
		return true
	}

	var sds bool = len(ol) > 0 && !justDExi(ol)

	if sds {
		Rmu.Lock()
		Printf("checking %s (%s) -> %s (%s), %s\n", sd.ST.Vl, sd.ST.Fp(), dd.ST.Vl, dd.ST.Fp(), rd)
		for op, il := range ol {
			Printf("%s: %d items\n", OpCodes[op], len(il))
		}
		Rmu.Unlock()
	} else {
		// Printf("%d %s\n", Dstats.Scanned.Dirs, rd)
	}

	if _, fnd := ol[DCrt]; fnd {
		if err := os.MkdirAll(dd.Fp(), 0666); err == nil {
			Printf("created dir %s\n", dd.Fp())
			Rmu.Lock()
			Dstats.Copied.Dirs++
			Rmu.Unlock()
		} else {
			Printf("failed to create dir %s; %s\n", dd.Fp(), err.Error())
			Rmu.Lock()
			Dstats.Errors++
			Rmu.Unlock()
			errs = append(errs, err)
			return
		}
	}

	var syncfunc = func(v DE) {
		var srd = filepath.Join(rd, v.Fname)
		errs2 := SyncTree(src, dst, srd)
		if len(errs2) > 0 {
			errs = append(errs, errs2...)
		}
	}

	var delfunc = func(v DE) {
		var ndd = dd.SubFile(v.Fname)
		if chkDeletable(ndd.Fp()) {
			if err := os.Remove(ndd.Fp()); err == nil {
				Printf("deleted file %s\n", ndd.Fp())
				Rmu.Lock()
				Dstats.Deleted.Files++
				Dstats.Deleted.Bytes += v.Size
				Rmu.Unlock()
			} else {
				Printf("failed to delete file %s; %s\n", ndd.Fp(), err.Error())
				Rmu.Lock()
				Dstats.Errors++
				Rmu.Unlock()
				errs = append(errs, err)
			}
		}
	}

	var copyfunc = func(v DE) {
		var ndd1 = sd.SubFile(v.Fname)
		var ndd2 = dd.SubFile(v.Fname)
		if chkCopyable(ndd2.Fp()) {
			if _, err := CopyFile(ndd1.Fp(), ndd2.Fp()); err == nil {
				Printf("copied file %s\n", ndd1.Fp())
				Rmu.Lock()
				Dstats.Copied.Files++
				Dstats.Copied.Bytes += v.Size
				Rmu.Unlock()
			} else {
				Printf("failed to copy file %s; %s\n", ndd1.Fp(), err.Error())
				Rmu.Lock()
				Dstats.Errors++
				Rmu.Unlock()
				errs = append(errs, err)
			}
		} else {
			errs = append(errs, errors.New("file not copyable in new-file"))
		}
	}

	if dl, ok := ol[FMis]; ok {
		for _, v := range dl {
			delfunc(v)
		}
	}

	if dl, ok := ol[DMis]; ok {
		for _, v := range dl {
			syncfunc(v)
		}
	}

	if _, ok := ol[DDel]; ok {
		if err := os.Remove(dd.Fp()); err == nil {
			Printf("deleted dir %s\n", dd.Fp())
			Rmu.Lock()
			Dstats.Deleted.Dirs++
			Rmu.Unlock()
			if sds {
				PrintStats()
			}
			return
		} else {
			Printf("failed to delete dir %s; %s\n", dd.Fp(), err.Error())
			Rmu.Lock()
			Dstats.Errors++
			Rmu.Unlock()
			errs = append(errs, err)
			if sds {
				PrintStats()
			}
			return
		}
	}

	if dl, ok := ol[FNew]; ok {
		for _, v := range dl {
			copyfunc(v)
		}
	}
	if dl, ok := ol[FExi]; ok {
		for _, v := range dl {
			copyfunc(v)
		}
	}

	if sds {
		PrintStats()
	}

	if dl, ok := ol[DNew]; ok {
		for _, v := range dl {
			syncfunc(v)
		}
	}

	if dl, ok := ol[DExi]; ok {
		for _, v := range dl {
			syncfunc(v)
		}
	}

	return
}
