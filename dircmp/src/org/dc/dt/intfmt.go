package dt

import (
	"fmt"
	"math"
)

func FmtInt2(n int64, lbl string) string {
	var exp = int(math.Ceil(math.Log10(float64(n))))
	if exp <= 3 {
		return fmt.Sprintf("%1.0f %s", float64(n), lbl)
	} else if exp <= 6 {
		return fmt.Sprintf("%1.1fK %s", float64(n)/1E3, lbl)
	} else if exp <= 9 {
		return fmt.Sprintf("%1.1fM %s", float64(n)/1E6, lbl)
	} else if exp <= 12 {
		return fmt.Sprintf("%1.1fG %s", float64(n)/1E9, lbl)
	}
	return "err"
}

func FmtInt(n int, lbl string) string {
	return FmtInt2(int64(n), lbl)
}
