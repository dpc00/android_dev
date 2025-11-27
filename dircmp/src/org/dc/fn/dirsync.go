package fn

import (
	_ "io"
	"log"
	"os"
	"path/filepath"

	"errors"

	"org/dc/dt"
)

func delDir(dd *dt.DItem) error {
	var err = os.RemoveAll(dd.Fp())
	return err
}

func SyncTree(st1, st2 dt.ST, rd string) (errs []error) {
	var sd = st1.SDir(rd)
	var dd = st2.SDir(rd)
	var sc = sd.GetContents()
	var dc = dd.GetContents()

	var ol = OpList(sc, dc)
	errs = []error{}

	var justDExi = func(ol dt.OpList) bool {
		for k := range ol {
			if k != dt.DExi {
				return false
			}
		}
		return true
	}

	var sds bool = len(ol) > 0 && !justDExi(ol)

	if sds {
		dt.Rmu.Lock()
		log.Printf("checking %s -> %s, %s\n", sd.ST.String(), dd.ST.String(), rd)
		for op, il := range ol {
			log.Printf("%s: %d items\n", dt.OpCodes[op], len(il))
		}
		dt.Rmu.Unlock()
	} else {
		//log.Printf("%d %s\n", dt.Dstats.Scanned.Dirs, rd)
	}

	if _, fnd := ol[dt.DCrt]; fnd {
		if err := os.MkdirAll(dd.Fp(), 0666); err == nil {
			log.Printf("created dir %s\n", dd.Fp())
			dt.Rmu.Lock()
			dt.Dstats.Copied.Dirs++
			dt.Rmu.Unlock()
		} else {
			log.Printf("failed to make dir %s; %s\n", dd.Fp(), err.Error())
			dt.Rmu.Lock()
			dt.Dstats.Errors++
			dt.Rmu.Unlock()
			errs = append(errs, err)
			return
		}
	}

	for _, v := range ol[dt.DMis] {
		var ndd = dd.SubDir(v.Fname)
		if err := delDir(ndd); err == nil {
			log.Printf("deleted dir %s\n", ndd.Fp())
			dt.Rmu.Lock()
			dt.Dstats.Deleted.Dirs++
			dt.Rmu.Unlock()
		} else {
			log.Printf("failed to delete %s; %s\n", ndd.Fp(), err.Error())
			dt.Rmu.Lock()
			dt.Dstats.Errors++
			dt.Rmu.Unlock()
			errs = append(errs, err)
		}
	}
	for _, v := range ol[dt.DNew] {
		var srd = filepath.Join(rd, v.Fname)
		if errs2 := SyncTree(st1, st2, srd); len(errs2) == 0 {
			dt.Rmu.Lock()
			dt.Dstats.Copied.Dirs++
			dt.Rmu.Unlock()
		} else {
			errs = append(errs, errs2...)
		}
	}
	for _, v := range ol[dt.FMis] {
		var ndd = dd.SubFile(v.Fname)
		if chkDeletable(ndd.Fp()) {
			if err := os.Remove(ndd.Fp()); err == nil {
				log.Printf("deleted file %s\n", ndd.Fp())
				dt.Rmu.Lock()
				dt.Dstats.Deleted.Files++
				dt.Dstats.Deleted.Bytes += v.Size
				dt.Rmu.Unlock()
			} else {
				log.Printf("failed to delete file %s; %s\n", ndd.Fp(), err.Error())
				dt.Rmu.Lock()
				dt.Dstats.Errors++
				dt.Rmu.Unlock()
				errs = append(errs, err)
			}
		}
	}
	for _, v := range ol[dt.FNew] {
		var ndd1 = sd.SubFile(v.Fname)
		var ndd2 = dd.SubFile(v.Fname)
		if chkCopyable(ndd2.Fp()) {
			if _, err := dt.WindowsCopyFile(ndd1.Fp(), ndd2.Fp()); err == 0 {
				log.Printf("copied file %s\n", ndd1.Fp())
				dt.Rmu.Lock()
				dt.Dstats.Copied.Files++
				dt.Dstats.Copied.Bytes += v.Size
				dt.Rmu.Unlock()
			} else {
				log.Printf("failed to copy file %s; %s\n", ndd1.Fp(), err.Error())
				dt.Rmu.Lock()
				dt.Dstats.Errors++
				dt.Rmu.Unlock()
				errs = append(errs, errors.New(err.Error()))
			}
		} else {
			errs = append(errs, errors.New("file not copyable in new-file"))
		}
	}
	for _, v := range ol[dt.FExi] {
		var ndd1 = sd.SubFile(v.Fname)
		var ndd2 = dd.SubFile(v.Fname)
		if chkCopyable(ndd2.Fp()) {
			if _, err := dt.WindowsCopyFile(ndd1.Fp(), ndd2.Fp()); err == 0 {
				log.Printf("copied file %s\n", ndd1.Fp())
				dt.Rmu.Lock()
				dt.Dstats.Copied.Files++
				dt.Dstats.Copied.Bytes += v.Size
				dt.Rmu.Unlock()
			} else {
				log.Printf("failed to copy file %s; %s\n", ndd1.Fp(), err.Error())
				dt.Rmu.Lock()
				dt.Dstats.Errors++
				dt.Rmu.Unlock()
				errs = append(errs, errors.New(err.Error()))
			}
		} else {
			errs = append(errs, errors.New("file not copyable in copy-file"))
		}
	}
	for _, v := range ol[dt.DExi] {
		var srd = filepath.Join(rd, v.Fname)
		if errs2 := SyncTree(st1, st2, srd); len(errs2) > 0 {
			errs = append(errs, errs2...)
		}
	}

	if sds {
		dt.PrintStats()
	}
	return
}

func chkDeletable(fp2 string) bool {
	if x, _ := fileExists(fp2); x {
		return isWritable(fp2)
	} else {
		return false
	}
}

func chkCopyable(fp2 string) bool {
	if x, _ := fileExists(fp2); x {
		return isWritable(fp2)
	} else {
		return true
	}
}

func isWritable(fp string) bool {
	if !_isWritable(fp) {
		var v1, err = os.Stat(fp)
		if err == nil {
			var fm = v1.Mode() & os.ModePerm
			os.Chmod(fp, fm|0666)
		}
		return _isWritable(fp)
	} else {
		return true
	}
}

func _isWritable(fp string) bool {
	var v1, err = os.Stat(fp)
	if err == nil {
		var fm = v1.Mode() & os.ModePerm
		if fm&0222 == 0222 {
			return true
		}
	}
	return false
}

func fileExists(fp string) (bool, error) {
	_, err := os.Stat(fp)
	if err == nil {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return true, err
}
