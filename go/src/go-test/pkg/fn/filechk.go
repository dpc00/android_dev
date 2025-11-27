package fn

import (
	"os"
)

func chkDeletable(fp2 string) bool {
	if x, _ := fileExists(fp2); x {
		return isWritable(fp2)
	} else {
		return false
	}
}

func chkCopyable(fp2 string) bool {
	if x, _ := fileExists(fp2); x {
		return isWritable(fp2)
	} else {
		return true
	}
}

func isWritable(fp string) bool {
	if !_isWritable(fp) {
		var v1, err = os.Stat(fp)
		if err == nil {
			var fm = v1.Mode() & os.ModePerm
			os.Chmod(fp, fm|0666)
		}
		return _isWritable(fp)
	} else {
		return true
	}
}

func _isWritable(fp string) bool {
	var v1, err = os.Stat(fp)
	if err == nil {
		var fm = v1.Mode() & os.ModePerm
		if fm&0222 == 0222 {
			return true
		}
	}
	return false
}

func fileExists(fp string) (bool, error) {
	_, err := os.Stat(fp)
	if err == nil {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return true, err
}
