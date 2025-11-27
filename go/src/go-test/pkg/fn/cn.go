package fn

import (
	"fmt"
	"reflect"
	. "syscall"
	"unsafe"
	"sync"
)

func Cn(fp string, flags uint32, cf func(int, string), cnwg *sync.WaitGroup) {
	var buf = []uint16{}
	var bufsh = (*reflect.SliceHeader)(unsafe.Pointer(&buf))
	var fna = []uint16{}
	var fnash = (*reflect.SliceHeader)(unsafe.Pointer(&fna))
	var fp2 = fp
	//if strings.Index(fp, "\\") == -1 {
	//	fp2 += "\\*"
	//} else { fp2 += "*" }
	fp3, err1 := UTF16PtrFromString(fp2);
	if err1 != nil {
		fmt.Printf("%s\n", err1.Error())
		return
	}
	handle, err2 := CreateFile(
		fp3,
		FILE_LIST_DIRECTORY,
		FILE_SHARE_READ|FILE_SHARE_WRITE|FILE_SHARE_DELETE,
		nil,
		OPEN_EXISTING,
		FILE_FLAG_BACKUP_SEMANTICS,
		0)
	if err2 != nil {
		fmt.Printf("%s\n", err2.Error())
		return
	}
	if len(buf) == 0 {
		buf = make([]uint16, 6+32768, 6+32768)
	}
	var retlen uint32 = 0
	for {
		if err3 := ReadDirectoryChanges(handle, (*byte)(unsafe.Pointer(bufsh.Data)), uint32(uint32(len(buf))*uint32(unsafe.Sizeof(buf[0]))), true, flags, &retlen, nil, 0); err3 == nil && retlen > 0 {
			var p *FileNotifyInformation = (*FileNotifyInformation)(unsafe.Pointer(bufsh.Data))
			fnash.Len = 0
			fnash.Cap = bufsh.Cap - 6
			for {
				var action int = int(p.Action)
				var fnl int = int(p.FileNameLength >> 1)
				fnash.Len = fnl
				fnash.Data = uintptr(unsafe.Pointer(&p.FileName))
				var path = UTF16ToString(fna)
				cf(action, path)
				if p.NextEntryOffset > 0 {
					fnash.Cap -= int(p.NextEntryOffset)
					p = (*FileNotifyInformation)(unsafe.Pointer(uintptr(unsafe.Pointer(p)) + uintptr(p.NextEntryOffset)))
				} else {
					break
				}
			}
		} else {
			fmt.Printf("%s\n", err3.Error())
			break
		}
	}
	cnwg.Done()
}
