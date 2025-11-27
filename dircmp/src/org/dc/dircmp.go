package main

import (
	"fmt"
	"log"
	"strings"

	"org/dc/dt"
	"org/dc/fn"

	"os"
)

func init() {
	dt.Rts = map[string]dt.ST{}
	for i := int('D'); i < int('M'); i++ {
		vl, err := dt.GetVolumeInformation(string(i) + ":")
		if err == 0 {
			log.Printf("%s\n", vl)
			dt.Rts[vl] = dt.ST{vl, []string{string(i) + ":"}}
		}
	}
}

func findST(pth string) *dt.ST {
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
	for _, v := range dt.Rts {
		if v.Pth[0] == dl {
			return &v
		}
	}
	return nil
}

func getST(a string) *dt.ST {
	if strings.Contains(a, "\"") {
		fmt.Printf("param contains \"\n")
	}
	var sa = strings.Split(a, "\\")
	if st := findST(sa[0]); st != nil {
		return &dt.ST{st.GetVl(), sa}
	}
	return nil
}

func main() {
	if len(os.Args) < 2 {
		return
	}
	var args = os.Args[1:]

	var st1 = getST(args[0])
	var c1 = st1.SDir("").GetContents()

	var st2 = getST(args[1])
	var c2 = st2.SDir("").GetContents()

	var opl = fn.OpList(c1, c2)
	for k1, v1 := range opl {
		for _, v2 := range v1 {
			if k1 == dt.DCrt || k1 == dt.DDel {
				fmt.Printf("%s %s\n", dt.OpCodes[k1], v2.Fname)
			} else {
				fmt.Printf("%s %s\n", dt.OpCodes[k1], v2.Fname)
			}
		}
	}
}
