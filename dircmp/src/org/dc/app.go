// dir sync program in go
package main

import (
	"sync"
	"time"

	"org/dc/dt"
	"org/dc/fn"

	"fmt"
	"log"
	"os"
	"strings"
)

func FlashBackups1() {
	if len(dt.Rts) < 2 {
		panic("not enough src/dst found")
	}

	var rd = ""
	var wg sync.WaitGroup = sync.WaitGroup{}

	wg.Add(len(dt.Rts) - 1)
	var st1 = dt.Rts["CODE0"]
	for k, v := range dt.Rts {
		if k != "CODE0" {
			var st2 = v
			go func() { fn.SyncTree(st1, st2, rd); wg.Done() }()
		}
	}

	wg.Wait()
	dt.Rmu.Lock()
	log.Printf("%s\n", strings.Repeat("=", 20))
	dt.PrintStats()
	dt.Rmu.Unlock()
}

var logf *os.File

func initLog() {
	var logf, err = os.OpenFile("dircmp.log", os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		log.Fatal(err)
	}
	log.SetOutput(logf)
}

func init() {
	initLog()

	dt.Rts = map[string]dt.ST{}
	for i := int('D'); i < int('M'); i++ {
		vl, err := dt.GetVolumeInformation(string(i) + ":")
		if err == 0 {
			log.Printf("%s\n", vl)
			dt.Rts[vl] = dt.ST{vl, []string{string(i) + ":"}}
		}
	}
}

func main2() {
	defer logf.Close()

	//fn.Pathgen()
	//fn.PrintExecPaths()

	dt.Rs.T1 = time.Now().UnixNano()
	// fn.GitBackups()

	dt.Rs.T2 = time.Now().UnixNano()

	//fn.MakeCCLs()
	//fn.PrintRBs()

	FlashBackups1()

	dt.Rs.T3 = time.Now().UnixNano()

	dt.Rs.S = dt.Dstats

	log.Printf("time for git backup %04.1f secs.\n", float64(dt.Rs.T2-dt.Rs.T1)/1.0E9)
	log.Printf("time for flash backups %04.1f secs.\n", float64(dt.Rs.T3-dt.Rs.T2)/1.0E9)
	log.Printf("cache hits: %d misses: %d\n", dt.Hits, dt.Misses)

	fmt.Printf("time for git backup %04.1f secs.\n", float64(dt.Rs.T2-dt.Rs.T1)/1.0E9)
	fmt.Printf("time for flash backups %04.1f secs.\n", float64(dt.Rs.T3-dt.Rs.T2)/1.0E9)
	fmt.Printf("cache hits: %d misses: %d\n", dt.Hits, dt.Misses)
}
