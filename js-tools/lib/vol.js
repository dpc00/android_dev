var utils = require("utils");
var util = require("util");
var path = require("path");

var dls;

function getDLs() {
  dls = {};
  ["C", "D", "E", "F", "G", "H"].forEach(function (dl) {
    var rv = utils.dos2("vol " + dl + ":");
    var ra = rv[0].split(/[\r\n]+/);
    ra.forEach(function (l) {
      if (l.startsWith(" Volume in drive ")) {
        var drv = l.substring(17, 18);
        var s = l.substring(22);
        if (!s.startsWith(" no label.")) {
          dls[s.trim()] = drv + ":";
        }
      }
    });
  });
}

function getDLs2() {
  dls = {};
  var rv = utils.dos2("wmic VOLUME where drivetype=2 get label,driveletter");
  var ra = rv[0].split(/[\r\n]+/);
  ra.slice(1).forEach(function (ln) {
    // console.log(ln);
    var drv = ln.substring(0, 2);
    var vol = ln.substring(10).trim();
    if (vol.length > 0) {
      dls[vol] = drv;
    }
  });
}

function findDL(vl) {
  if (!dls) getDLs2();
  return dls[vl];
}
module.exports.findDL = findDL;

function printDLs() {
  if (!dls) getDLs2();
  utils.log(util.inspect(dls));
}
module.exports.printDLs = printDLs;
