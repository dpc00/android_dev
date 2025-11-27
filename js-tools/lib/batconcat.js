/// <ref path="typings/main.d.ts"/>

var fs = require("fs");
var utils = require("utils");
var path = require("path");
var diskutils = require("diskutils");

function run() {
  const crlf = "\r\n";
  diskutils
    .filesList(__dirname.substring(0, 3) + "\\.bat", [".bat"])
    .then(function (bfl) {
      var abl = [];
      abl.push("shift");
      abl.push("goto %0");
      abl.push("goto exit");
      bfl.forEach(function (bf, i, bfl) {
        console.log(i, bf.fp, bf.size);
        var s = fs.readFileSync(bf.fp, "utf8");
        var la = s
          .split(/[\r\n]+/)
          .map((s) => {
            return s.trim();
          })
          .filter((s) => {
            return s.length > 0;
          });
        var lbl = ":" + path.basename(bf.fp).split(".bat")[0].toUpperCase();
        if (lbl !== ":PLAUNCH" && lbl !== ":ALL") {
          abl.push(lbl);
          la.forEach((l) => {
            abl.push("\t" + l);
          });
          abl.push("goto exit");
          abl.push("");
        }
      });
      abl.push(":exit");
      var txt = "";
      abl.forEach((l) => {
        txt += l + crlf;
      });
      fs.writeFileSync(__dirname.substring(0, 3) + "all.bat", txt, {
        encoding: "ascii",
      });
    });
}
module.exports.run = run;
