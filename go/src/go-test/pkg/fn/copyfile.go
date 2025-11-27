package fn

import (
	"io"
	"fmt"
	"os"
)

func CopyFile(p1, p2 string) (int64, error) {
	var (
		bw   int64
		err1 error
		err2 error
		err3 error
		err4 error
		err5 error
		err6 error
		err7 error
		err8 error
		err9 error
		sfi1 os.FileInfo
		sfi2 os.FileInfo
	)
	sfi1, err1 = os.Stat(p1)
	if err1 != nil {
		fmt.Printf("%s\n", err1.Error())
		return 0, err1
	}

	sfi2, err2 = os.Stat(p2)
	if err2 == nil && sfi2.Mode().IsRegular() {
		if sfi2.Mode().Perm()&0222 != 0222 {
			fmt.Println("")
			err3 = os.Chmod(p2, 0666)
			if err3 != nil {
				fmt.Printf("%s\n", err3.Error())
			}
		}
	} else if err2 != nil {
		if !os.IsNotExist(err2) {
			fmt.Printf("%s\n", err2.Error())
			return 0, err2
		}
	}
	if os.SameFile(sfi1, sfi2) {
		fmt.Printf("same file %s %s\n", p1, p2)
		return 0, os.ErrInvalid
	}
	var f1, f2 *os.File
	f1, err4 = os.OpenFile(p1, os.O_RDONLY, 0666)
	if err4 != nil {
		fmt.Printf("%s\n", err4.Error())
		return 0, err4
	}
	f2, err5 = os.OpenFile(p2, os.O_CREATE|os.O_TRUNC|os.O_WRONLY, 0666)
	if err5 != nil {
		fmt.Printf("%s\n", err5.Error())
		return 0, err5
	}
	bw, err6 = io.CopyBuffer(f2, f1, make([]byte, 1024*1024*32-64*1024))
	if err6 != nil {
		fmt.Printf("%s\n", err6.Error())
		return 0, err6
	}
	err7 = f2.Sync()
	if err7 != nil {
		fmt.Printf("%s\n", err7.Error())
		return 0, err7
	}
	err8 = f2.Close()
	if err8 != nil {
		fmt.Printf("%s\n", err8.Error())
		return 0, err8
	}
	err9 = f1.Close()
	if err9 != nil {
		fmt.Printf("%s\n", err9.Error())
		return 0, err9
	}
	chTime(p1, p2)
	return bw, nil
}

func chTime(p1, p2 string) error {
	var (
		err1, err2, err3 error
		sfi1, sfi2       os.FileInfo
	)
	sfi1, err1 = os.Stat(p1)
	if err1 != nil {
		fmt.Printf("%s\n", err1.Error())
		return err1
	}
	sfi2, err2 = os.Stat(p2)
	if err2 != nil {
		fmt.Printf("%s\n", err2.Error())
		return err2
	}
	err3 = os.Chtimes(p2, sfi2.ModTime(), sfi1.ModTime())
	if err3 != nil {
		fmt.Printf("%s\n", err3.Error())
		return err3
	}
	return nil
}
