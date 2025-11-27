package dt

import (
	"log"
	"syscall"
	"unsafe"
)

func WindowsCopyFile(src, dst string) (bool, syscall.Errno) {
	srcfn, _ := syscall.UTF16FromString(src)
	dstfn, _ := syscall.UTF16FromString(dst)
	ret, _, we := syscall.Syscall(
		uintptr(copyFile),
		3,
		uintptr(unsafe.Pointer(&srcfn[0])),
		uintptr(unsafe.Pointer(&dstfn[0])),
		uintptr(0),
	)
	if ret == 0 {
		if we != 0 {
			log.Printf("copyfile we: %s\n", we.Error())
		}
		return false, we
	}
	return true, we
}

func GetVolumeInformation(dl string) (string, syscall.Errno) {
	rpn, _ := syscall.UTF16FromString(dl + "\\")

	var vl = [330]uint16{}
	vls := len(vl)

	var vsn = [1]uint32{0}
	var mcl = [1]uint32{0}
	var fsf = [1]uint32{0}
	var fsn = [330]uint16{}
	fsns := len(fsn)

	ret, _, we := syscall.Syscall9(
		uintptr(getVolumeInformation),
		8,
		uintptr(unsafe.Pointer(&rpn[0])), // in
		uintptr(unsafe.Pointer(&vl[0])),  // out
		uintptr(vls),                     // in
		uintptr(unsafe.Pointer(&vsn[0])), // out dword
		uintptr(unsafe.Pointer(&mcl[0])), // out dword
		uintptr(unsafe.Pointer(&fsf[0])), // out dword
		uintptr(unsafe.Pointer(&fsn[0])), // out name
		uintptr(fsns),
		0)
	if ret == 0 {
		if we != 0 {
			log.Println("getvolumeinformation we: ", we.Error())
		}
		return "", we
	}
	return syscall.UTF16ToString(vl[:]), we
}
