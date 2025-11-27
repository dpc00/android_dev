package dt

import (
	"fmt"
	"os"
	"time"
)

func (de DE) String() string {
	return fmt.Sprintf("%s \"%s\" %s %d", ETName[de.EType], de.Fname, de.Mtime.Local().Format(time.UnixDate), de.Size)
}

func FromFI(des os.FileInfo) *DE {
	de := &DE{
		EType: func() EType {
			if des.Mode().IsDir() {
				return Dir
			}
			if des.Mode().IsRegular() {
				return File
			}
			return Unknown
		}(),
		Fname: des.Name(),
		Mtime: des.ModTime(),
		Size:  des.Size(),
	}
	return de
}

func (de2 DE) IsUpToDateWith(de1 DE) bool {
	var v3 = de2.Mtime.Sub(de1.Mtime).Nanoseconds()
	if v3 > 2.0E9 || v3 < -2.0E9 {
		return false
	}
	return de2.Size == de1.Size
}
