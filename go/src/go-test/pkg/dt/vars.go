package dt

import (
	. "sync"
	"syscall"
)

var Rmu Mutex = *new(Mutex)
var Cnwg WaitGroup

var Rts map[string]*ST

var (
	kernel32, _             = syscall.LoadLibrary("kernel32.dll")
	getVolumeInformation, _ = syscall.GetProcAddress(kernel32, "GetVolumeInformationW")
	copyFile, _             = syscall.GetProcAddress(kernel32, "CopyFileW")
)

func init() {
	Rts = map[string]*ST{}
	for i := int('D'); i < int('Z'); i++ {
		vl, err := GetVolumeInformation(string(i) + ":")
		if err == 0 {
			// fmt.Printf("%s\n", vl)
			if len(vl) > 0 && vl[0:4] == "CODE" {
				Rts[vl] = &ST{vl, []string{string(i) + ":"}, []string{}, nil, WaitGroup{}}
			}
		}
	}
}
