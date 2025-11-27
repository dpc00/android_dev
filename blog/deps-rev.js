const fs = require('fs');

// t=JSON.stringify("[{'dfg':[]}]",null,4);
// console.log(t);

let rawdata = fs.readFileSync('deps.json');
let deps = JSON.parse(rawdata);
r = {};
for (var i of Object.keys(deps)) {
    l = deps[i];
    for (var li of l) {
        if(li in r) {
            r[li].push(i);
        } else {
            r[li] = [i];
        }
    }
}
depsrev = JSON.stringify(r, null, 4);
fs.writeFileSync("deps-rev.json",depsrev);