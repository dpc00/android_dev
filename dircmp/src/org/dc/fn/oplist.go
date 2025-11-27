package fn

import (
	"org/dc/dt"
)

func OpList(sContents, dContents *dt.Contents) (ol dt.OpList) {
	var scf = sContents.Files
	var scd = sContents.Dirs
	var dcf = dContents.Files
	var dcd = dContents.Dirs

	var add = func(oc dt.OpCode, de1 dt.DE) {
		_, ok := ol[oc]
		if !ok {
			ol[oc] = []dt.DE{de1}
		} else {
			ol[oc] = append(ol[oc], de1)
		}
	}

	ol = dt.OpList{}

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
		add(dt.DCrt, dt.DE{})
		for _, de1 := range scf {
			add(dt.FNew, de1)
		}
		for _, de1 := range scd {
			add(dt.DNew, de1)
		}
	case 2: // missing
		for _, de2 := range dcd {
			add(dt.DMis, de2)
		}
		for _, de2 := range dcf {
			add(dt.FMis, de2)
		}
		add(dt.DDel, dt.DE{})
	case 3: // both exist
		for _, de2 := range dcd { // delete missing Dirs
			var _, f1 = scd[de2.Fname]
			var _, f2 = scf[de2.Fname]
			if !f1 || f2 {
				add(dt.DMis, de2)
			}
		}
		for _, de2 := range dcf { // delete missing Files
			var _, f1 = scf[de2.Fname]
			var _, f2 = scd[de2.Fname]
			if !f1 || f2 {
				add(dt.FMis, de2)
			}
		}
		for _, de1 := range scf { // possibly copy modified/new Files
			var de2, f1 = dcf[de1.Fname]
			if !f1 { // new file
				add(dt.FNew, de1)
			} else {
				if !de2.IsUpToDateWith(de1) { // modified
					add(dt.FExi, de1)
				}
			}
		}
		for _, de1 := range scd {
			var _, f2 = dcd[de1.Fname]
			if !f2 {
				add(dt.DNew, de1)
			} else {
				add(dt.DExi, de1)
			}
		}
	}
	return ol
}
