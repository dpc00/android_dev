package fn

import (
	"log"
	"os"
	"os/exec"
	"sort"
	"strings"

	"org/dc/dt"
)

func git(args ...string) {
	var cmd = *exec.Command("git.exe", args...)
	s, e := cmd.CombinedOutput()
	dt.LogPrintlns(string(s))
	if e != nil {
		log.Println(e.Error())
	}
}

func git2(args ...string) []string {
	var cmd = *exec.Command("git.exe", args...)
	s, e := cmd.CombinedOutput()
	dt.LogPrintlns(string(s))
	if e != nil {
		log.Println(e.Error())
	}
	var sa = strings.Split(string(s), "\n")
	return sa
}

func backup() {
	var sa []string = git2("status","--porcelain", "--untracked-files=all")
	for _, s := range sa {
		fp := s[3:]
		git("add", "-A", fp)
	}
	git("commit", "-m", "abcde")
	git("push", "origin", "master")
}

func GitBackups() {
	var st1 dt.ST = dt.Rts["CODE0"]
	var d *dt.DItem = st1.SDir("Projects")
	var gdl []dt.DItem = Find(d, "\\.git$")
	var cd, ocd string
	var err error

	log.Println(gdl)
	sort.Sort(sort.Reverse(dt.DISlice(gdl)))
	ocd, err = os.Getwd()
	if err == nil {
		for _, gdp := range gdl {
			if gdp.EType == dt.Dir {
				cd = gdp.Parent().Fp()
				log.Println("git backup " + cd)
				err := os.Chdir(cd)
				if err == nil {
					backup()
				}
			}
		}
		err = os.Chdir(ocd)
	}
}
