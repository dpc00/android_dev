package fn

import (
	. "../../pkg/dt"
	"fmt"
	"sort"
)

func noDupsDirs(elements []DItem) []DItem {
	// Use map to record duplicates as we find them.
	encountered := make(map[string]bool)
	result := []DItem{}

	var v DItem
	for _, v = range elements {
		if v.EType == File {
			var k = v.Parent().Fp()
			if _, ok := encountered[k]; !ok {
				encountered[k] = true
				result = append(result, *v.Parent())
			}
		}
	}
	return result
}

func Pathgen() []DItem {
	var st1 *ST = Rts["CODE0"]
	var d *DItem = st1.SDir("")
	// .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC
	//var sre = "\\.acm$|\\.ax$|\\.bat$|\\.cmd$|\\.com$|\\.cpl$|\\.dll$|\\.drv$|\\.efi$|\\.exe$|\\.js$|\\.jse$|\\.msc$|\\.mui$|\\.ocx$|\\.scr$|\\.sys$|\\.tsp$|\\.vbe$|\\.vbs$|\\.wsf|\\.wsh$"
	var sre = "\\.bat$|\\.cmd$|\\.com$|\\.dll$|\\.exe$"
	var gdl []DItem = Find(d, sre)

	gdl = noDupsDirs(gdl)
	sort.Sort(DISlice(gdl))

	for i, d := range gdl {
		var k = "execdirs:" + d.Rp()
		fmt.Printf("%s %d\n", k, i)
		//DSdb.Put([]byte(k), []byte(strconv.Itoa(i)), nil)
	}

	return gdl
}
