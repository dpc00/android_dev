package dt

import (
	"bytes"
	"encoding/gob"
	"fmt"
	"log"
	"strings"
	"sync"
)

func LogPrintlns(s string) {
	var sa = strings.Split(s, "\n")
	for _, s2 := range sa {
		log.Printf("%s\n", s2)
	}
}

func PrintStats() {
	LogPrintlns(Dstats.String())
}

func Marshal(v interface{}) ([]byte, error) {
	var b bytes.Buffer
	enc := gob.NewEncoder(&b)
	err := enc.Encode(v)
	if err != nil {
		return nil, err
	}
	return b.Bytes(), nil
}

func Unmarshal(b []byte, v interface{}) error {
	r := bytes.NewReader(b)
	dec := gob.NewDecoder(r)
	return dec.Decode(v)
}

func (oc OpCode) String() string {
	return OpCodes[int(oc)]
}

func init() {
	Mu2 = *new(sync.Mutex)
	Mu = *new(sync.Mutex)
	Rmu = *new(sync.Mutex)
	Wg = *new(sync.WaitGroup)
}

func (p DISlice) Len() int           { return len(p) }
func (p DISlice) Less(i, j int) bool { return p[i].Fp() < p[j].Fp() }
func (p DISlice) Swap(i, j int)      { p[i], p[j] = p[j], p[i] }

func (ol *OpList) String() string {
	var s string = " -- OpList\n"
	for k, v := range *ol {
		s += fmt.Sprintf("  %s:\n", k)
		for i, v2 := range v {
			s += fmt.Sprintf("\t%d: %s\n", i, v2.String())
		}
	}
	return s
}
