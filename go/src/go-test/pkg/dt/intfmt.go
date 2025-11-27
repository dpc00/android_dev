package dt

import (
	"fmt"
)

func FmtInt2(n int64, lbl string) string {
	return fmt.Sprintf("%d %s", n, lbl)
}

func FmtInt(n int, lbl string) string {
	return FmtInt2(int64(n), lbl)
}
