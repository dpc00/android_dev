// dir sync program in go
package main

import (
	. "../../pkg/dt"
	. "../../pkg/fn"
	"fmt"
	"os"
	"path/filepath"
	. "syscall"
	. "time"
)

var flags uint32 = FILE_NOTIFY_CHANGE_FILE_NAME |
	FILE_NOTIFY_CHANGE_DIR_NAME |
	FILE_NOTIFY_CHANGE_ATTRIBUTES |
	FILE_NOTIFY_CHANGE_SIZE |
	FILE_NOTIFY_CHANGE_LAST_WRITE |
	FILE_NOTIFY_CHANGE_LAST_ACCESS |
	FILE_NOTIFY_CHANGE_CREATION

func cnc(action int, path string) {
	switch action {
	case FILE_ACTION_ADDED:
		fallthrough
	case FILE_ACTION_MODIFIED:
		var sd = src.SFile(path)
		var fi os.FileInfo
		var err error
		if fi, err = os.Stat(sd.Fp()); err == nil {
			if fi.IsDir() {
				doSyncs(path)
			} else {
				doSyncs(filepath.Dir(path))
			}
		} else {
			if v, ok := err.(*os.PathError); ok {
				if v.Op == "CreateFile" && v.Err.Error() == "The system cannot find the file specified." {
					// doSyncs(path)
					doSyncs(filepath.Dir(path))
				} else {
					fmt.Printf("v.Op: %s v.Err.Error(): %s\n", v.Op, v.Err.Error())
				}
			} else {
				fmt.Printf("%s\n", err.Error())
			}
		}
	case FILE_ACTION_REMOVED:
		fallthrough
	case FILE_ACTION_RENAMED_OLD_NAME:
		fallthrough
	case FILE_ACTION_RENAMED_NEW_NAME:
		doSyncs(path)
		doSyncs(filepath.Dir(path))
	}
}

var Rs RunStats
var src *ST

func Index(vs []string, t string) int {
	for i, v := range vs {
		if v == t {
			return i
		}
	}
	return -1
}

func wait() {
	for k, _ := range Rts {
		var dst *ST = Rts[k]
		if k != "CODE0" && k[0:4] == "CODE" {
			dst.Wg.Wait()
		}
	}
}

func doSyncs(rd string) {
	for k, _ := range Rts {
		var dst *ST = Rts[k]
		if k != "CODE0" && k[0:4] == "CODE" {
			if Index(dst.Q, rd) == -1 {
				fmt.Printf("sync event of: %s to %s rd: %s\n", src.Fp(), dst.Fp(), rd)
				dst.Q = append(dst.Q, rd)
			}
			if dst.Sf == nil {
				dst.Run(src, SyncTree)
				PrintStats()
			}
		}
	}
}

func main() {

	//Pathgen()
	//PrintExecPaths()

	Rs.T2 = Now().UnixNano()

	//MakeCCLs()
	//PrintRBs()

	src = Rts["CODE0"]

	Cnwg.Add(1)
	go Cn(src.Fp(), flags, cnc, &Cnwg)

	doSyncs("")
	wait()

	Rs.T3 = Now().UnixNano()

	Rs.S = Dstats
	fmt.Printf("==================\n")
	PrintStats()
	fmt.Printf("==================\n")
	fmt.Printf("time for flash backups %04.1f secs.\n", float64(Rs.T3-Rs.T2)/1.0E9)
	fmt.Printf("cache hits: %d misses: %d\n", Hits, Misses)

	Cnwg.Wait()
}
