package fn

import "../../pkg/dt"
import "fmt"

type OpList map[OpCode][]dt.DE

type OpCode uint8

const (
	noOp OpCode = iota
	DCrt
	DMis
	FMis
	FNew
	FExi
	DNew
	DExi
	DDel
)

var OpCodes = []string{
	"noOp",
	"DCrt",
	"DMis",
	"FMis",
	"FNew",
	"FExi",
	"DNew",
	"DExi",
	"DDel",
}

func (oc OpCode) String() string {
	return OpCodes[int(oc)]
}

func (ol *OpList) String() string {
	var s string = " -- OpList\n"
	for k, v := range *ol {
		s += fmt.Sprintf("  %s:\n", k)
		for i, v2 := range v {
			s += fmt.Sprintf("\t%d: %s\n", i, v2.String())
		}
	}
	return s
}

func MakeOpList(sContents, dContents *dt.Contents) (ol OpList) {
	var scf = sContents.Files
	var scd = sContents.Dirs
	var dcf = dContents.Files
	var dcd = dContents.Dirs

	var add = func(oc OpCode, de1 dt.DE) {
		_, ok := ol[oc]
		if !ok {
			ol[oc] = []dt.DE{de1}
		} else {
			ol[oc] = append(ol[oc], de1)
		}
	}

	ol = OpList{}

	if sContents.Blocked || dContents.Blocked {
		if dContents.Blocked {
		}
		return ol
	}

	var sc int
	if sContents.Dex {
		sc |= 1
	}
	if dContents.Dex {
		sc |= 2
	}

	switch sc {
	case 0: // both don't exist
	case 1: // new
		add(DCrt, dt.DE{})
		for _, de1 := range scf {
			add(FNew, de1)
		}
		for _, de1 := range scd {
			add(DNew, de1)
		}
	case 2: // missing
		for _, de2 := range dcd {
			add(DMis, de2)
		}
		for _, de2 := range dcf {
			add(FMis, de2)
		}
		add(DDel, dt.DE{})
	case 3: // both exist
		for _, de2 := range dcd { // delete missing Dirs
			var _, f1 = scd[de2.Fname]
			var _, f2 = scf[de2.Fname]
			if !f1 || f2 {
				add(DMis, de2)
			}
		}
		for _, de2 := range dcf { // delete missing Files
			var _, f1 = scf[de2.Fname]
			var _, f2 = scd[de2.Fname]
			if !f1 || f2 {
				add(FMis, de2)
			}
		}
		for _, de1 := range scf { // possibly copy modified/new Files
			var de2, f1 = dcf[de1.Fname]
			if !f1 { // new file
				add(FNew, de1)
			} else {
				if !de2.IsUpToDateWith(de1) { // modified
					add(FExi, de1)
				}
			}
		}
		for _, de1 := range scd {
			var _, f2 = dcd[de1.Fname]
			if !f2 {
				add(DNew, de1)
			} else {
				add(DExi, de1)
			}
		}
	}
	return ol
}
