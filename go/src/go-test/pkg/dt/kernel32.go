package dt

import (
	"fmt"
	"reflect"
	. "syscall"
	"time"
	"unsafe"
)

var modkernel32 = NewLazyDLL("kernel32.dll")
var procFindFirstFileW = modkernel32.NewProc("FindFirstFileW")
var procFindNextFileW = modkernel32.NewProc("FindNextFileW")
var procFindClose = modkernel32.NewProc("FindClose")

type WIN32_FIND_DATA struct {
	FileAttributes    uint32
	CreationTime      Filetime
	LastAccessTime    Filetime
	LastWriteTime     Filetime
	FileSizeHigh      uint32
	FileSizeLow       uint32
	Reserved0         uint32
	Reserved1         uint32
	FileName          [MAX_PATH]uint16
	AlternateFileName [14]uint16
}

func errnoErr(e Errno) error {
	switch e {
	case 0:
		return nil
	}
	return e
}

var uia = []uint16{}
var uiash = (*reflect.SliceHeader)(unsafe.Pointer(&uia))
var fd WIN32_FIND_DATA

func (fd WIN32_FIND_DATA) getFName() string {
	var fnl int = func() int {
		for i := 0; i < len(fd.FileName); i++ {
			if fd.FileName[i] == 0 {
				return i
			}
		}
		return len(fd.FileName)
	}()
	uiash.Cap = len(fd.FileName)
	uiash.Len = fnl
	uiash.Data = uintptr(unsafe.Pointer(&fd.FileName))
	return UTF16ToString(uia)
}

func (fd WIN32_FIND_DATA) getModTime() time.Time {
	return time.Unix(0, fd.LastWriteTime.Nanoseconds())
}

// const missing from ztypes_windows.go
const FILE_ATTRIBUTE_DEVICE = 64

// const FILE_ATTRIBUTE_COMPRESSED = 2048
// const FILE_ATTRIBUTE_OFFLINE = 4096
// const FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 8192
// const FILE_ATTRIBUTE_ENCRYPTED = 16384
// const FILE_ATTRIBUTE_INTEGRITY_STREAM = 32768
// const FILE_ATTRIBUTE_VIRTUAL = 65536
// const FILE_ATTRIBUTE_NO_SCRUB_DATA = 131072

func (fd WIN32_FIND_DATA) ToDE() (de *DE) {
	de = &DE{
		func(fa uint32) EType {
			var e1 bool = fa&(FILE_ATTRIBUTE_DEVICE|FILE_ATTRIBUTE_REPARSE_POINT) != 0
			var e2 bool = fd.Reserved0 == IO_REPARSE_TAG_SYMLINK
			if !e1 && !e2 {
				if (fa & FILE_ATTRIBUTE_DIRECTORY) != 0 {
					return Dir
				} else {
					return File
				}
			}
			return Unknown
		}(fd.FileAttributes),
		fd.getFName(),
		fd.getModTime(),
		int64(fd.FileSizeHigh)<<32 | (int64(fd.FileSizeLow) & 0xFFFFFFFF),
	}
	return
}

func (fd *WIN32_FIND_DATA) findFirstFile(name *uint16) (handle Handle, err error) {
	r0, _, e1 := Syscall(procFindFirstFileW.Addr(), 2, uintptr(unsafe.Pointer(name)), uintptr(unsafe.Pointer(fd)), 0)
	handle = Handle(r0)
	if handle == InvalidHandle {
		if e1 != 0 {
			err = errnoErr(e1)
		} else {
			err = EINVAL
		}
	}
	return
}

func (fd *WIN32_FIND_DATA) findNextFile(handle Handle) (err error) {
	r1, _, e1 := Syscall(procFindNextFileW.Addr(), 2, uintptr(handle), uintptr(unsafe.Pointer(fd)), 0)
	if r1 == 0 {
		if e1 != 0 {
			err = errnoErr(e1)
		} else {
			err = EINVAL
		}
	}
	return
}

func findClose(handle Handle) (err error) {
	r1, _, e1 := Syscall(procFindClose.Addr(), 1, uintptr(handle), 0, 0)
	if r1 == 0 {
		if e1 != 0 {
			err = errnoErr(e1)
		} else {
			err = EINVAL
		}
	}
	return
}

func ReadDir(fp string) ([]*DE, error) {
	var dea = []*DE{}
	var fp2 string
	if fp[len(fp)-1] == '\\' {
		fp2 = fp + "*"
	} else {
		fp2 = fp + "\\*"
	}
	ufp, err1 := UTF16FromString(fp2)
	if err1 != nil {
		fmt.Printf("%s\n", err1.Error())
		return dea, err1
	}
	handle, err2 := fd.findFirstFile((*uint16)(unsafe.Pointer(&ufp[0])))
	if err2 != nil {
		//fmt.Printf("%s\n", err2.Error())
		return dea, err2
	}
	if handle != InvalidHandle {
		defer findClose(handle)
	}
	var de *DE = fd.ToDE()
	if de.Fname != "." && de.Fname != ".." {
		dea = append(dea, de)
	}
	var err3 error
	for {
		err3 = fd.findNextFile(handle)
		if err3 != nil {
			if err3.Error() == "There are no more files." {
				err3 = nil
			} else {
				fmt.Printf("%s\n", err3.Error())
			}
			break
		}
		var de *DE = fd.ToDE()
		if de.Fname != "." && de.Fname != ".." {
			dea = append(dea, de)
		}
	}
	return dea, err3
}

func WindowsCopyFile(src, dst string) (int64, error) {
	srcfn, _ := UTF16FromString(src)
	dstfn, _ := UTF16FromString(dst)
	ret, _, we := Syscall(
		uintptr(copyFile),
		3,
		uintptr(unsafe.Pointer(&srcfn[0])),
		uintptr(unsafe.Pointer(&dstfn[0])),
		uintptr(0),
	)
	if ret == 0 {
		if we != 0 {
			// fmt.Printf("copyfile we: %s\n", we.Error())
		}
		return 0, errnoErr(we)
	}
	return 1, errnoErr(we)
}

func GetVolumeInformation(dl string) (string, Errno) {
	rpn, _ := UTF16FromString(dl + "\\")

	var vl = [330]uint16{}
	vls := len(vl)

	var vsn uint32
	var mcl uint32
	var fsf uint32
	var fsn = [330]uint16{}
	fsns := len(fsn)

	ret, _, we := Syscall9(
		uintptr(getVolumeInformation),
		8,
		uintptr(unsafe.Pointer(&rpn[0])), // in
		uintptr(unsafe.Pointer(&vl[0])),  // out
		uintptr(vls),                     // in
		uintptr(unsafe.Pointer(&vsn)),    // out dword
		uintptr(unsafe.Pointer(&mcl)),    // out dword
		uintptr(unsafe.Pointer(&fsf)),    // out dword
		uintptr(unsafe.Pointer(&fsn[0])), // out name
		uintptr(fsns),
		0)
	if ret == 0 {
		if we != 0 {
			// fmt.Println("getvolumeinformation we: ", we.Error())
		}
		return "", we
	}
	return UTF16ToString(vl[:]), we
}
