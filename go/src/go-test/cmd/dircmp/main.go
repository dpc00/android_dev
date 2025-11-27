package main

import (
	. "../../pkg/dt"
	. "../../pkg/fn"
	"fmt"
	"os"
	"strings"
	. "sync"
	"syscall"
	"unsafe"
)

var cmdline string

func init() {
	p := syscall.GetCommandLine()
	cmdline = syscall.UTF16ToString((*[0xffff]uint16)(unsafe.Pointer(p))[:])
}

func findST(pth string) *ST {
	var dl string
	if len(pth) > 1 && pth[1:2] == ":" {
		dl = pth[0:2]
	} else {
		if dir, err := os.Getwd(); err == nil && dir[1:2] == ":" {
			dl = dir[0:2]
		} else {
			return nil
		}
	}
	for _, v := range Rts {
		if v.Pth[0] == dl {
			return v
		}
	}
	return nil
}

func getST(a string) *ST {
	var sa = strings.Split(a, "\\")
	if st := findST(sa[0]); st != nil {
		return &ST{st.GetVl(), sa, []string{}, nil, WaitGroup{}}
	}
	return nil
}

func main() {
	if len(os.Args) < 3 {
		return
	}
	//	fmt.Printf("cmdline: %s\n", cmdline)
	//	for i, v := range os.Args {
	//		fmt.Printf("arg[%d]: %s\n", i, v)
	//	}
	var args = os.Args[1:]

	var st1 = getST(args[0])
	var c1 = st1.SDir("").GetContents()

	var st2 = getST(args[1])
	var c2 = st2.SDir("").GetContents()

	var opl = MakeOpList(c1, c2)
	for k1, v1 := range opl {
		for _, v2 := range v1 {
			if k1 == DCrt || k1 == DDel {
				fmt.Printf("%s %s\n", OpCodes[k1], v2.Fname)
			} else {
				fmt.Printf("%s %s\n", OpCodes[k1], v2.Fname)
			}
		}
	}
}
