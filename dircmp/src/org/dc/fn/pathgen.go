package fn

import (
	"log"
	"sort"

	"org/dc/dt"
)

func noDupsDirs(elements []dt.DItem) []dt.DItem {
	// Use map to record duplicates as we find them.
	encountered := make(map[string]bool)
	result := []dt.DItem{}

	var v dt.DItem
	for _, v = range elements {
		if v.EType == dt.File {
			var k = v.Parent().Fp()
			if _, ok := encountered[k]; !ok {
				encountered[k] = true
				result = append(result, *v.Parent())
			}
		}
	}
	return result
}

func Pathgen() []dt.DItem {
	var st1 dt.ST = dt.Rts["CODE0"]
	var d *dt.DItem = st1.SDir("")
	// .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC
	//var sre = "\\.acm$|\\.ax$|\\.bat$|\\.cmd$|\\.com$|\\.cpl$|\\.dll$|\\.drv$|\\.efi$|\\.exe$|\\.js$|\\.jse$|\\.msc$|\\.mui$|\\.ocx$|\\.scr$|\\.sys$|\\.tsp$|\\.vbe$|\\.vbs$|\\.wsf|\\.wsh$"
	var sre = "\\.bat$|\\.cmd$|\\.com$|\\.dll$|\\.exe$"
	var gdl []dt.DItem = Find(d, sre)

	gdl = noDupsDirs(gdl)
	sort.Sort(dt.DISlice(gdl))

	for i, d := range (gdl) {
		var k = "execdirs:" + d.Rp()
		log.Printf("%s %d\n", k, i)
		//dt.DSdb.Put([]byte(k), []byte(strconv.Itoa(i)), nil)
	}

	return gdl
}

