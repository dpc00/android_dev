package dt

import (
	"fmt"
	"time"
)

func (c *Contents) String() string {
	var s string = " -- Contents\n"
	s += fmt.Sprintf(" Dex: %t\n", c.Dex)
	s += fmt.Sprintf(" Blocked: %t\n", c.Blocked)
	s += fmt.Sprintf(" Ftime: %s\n", time.Unix(0,c.Ftime).Local().Format(time.UnixDate))
	s += fmt.Sprintf(" Utime: %s\n", time.Unix(0,c.Utime).Local().Format(time.UnixDate))
	s += fmt.Sprintf(" LCtime: %s\n", time.Unix(0,c.LCtime).Local().Format(time.UnixDate))
	var i = 0
	for _, v := range c.Files {
		s += fmt.Sprintf("\t%d: %s\n", i, v.String())
		i++
	}
	i = 0
	for _, v := range c.Dirs {
		s += fmt.Sprintf("\t%d: %s\n", i, v.String())
		i++
	}
	return s
}