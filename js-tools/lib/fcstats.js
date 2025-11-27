var utils = require("utils");

var pcnt = 0;
var colw = 12;

var fcstats = {
  dcpy: 0,
  ddel: 0,
  fcpy: 0,
  fdel: 0,
  bcpy: 0,
  bdel: 0,
};
module.exports.fcstats = fcstats;

var fcstats2 = {};

function cpy() {
  for (var k in fcstats) {
    fcstats2[k] = fcstats[k];
  }
}
module.exports.cpy = cpy;

function chk() {
  for (var k in fcstats) {
    if (fcstats2[k] != fcstats[k]) {
      cpy();
      return true;
    }
  }
  return false;
}
module.exports.chk = chk;

function clr() {
  for (var k in fcstats) {
    fcstats[k] = 0;
  }
  cpy();
}
module.exports.clr = clr;

function rightJ(str, len) {
  if (str.length < len) {
    for (; str.length < len; ) str = " " + str;
  }
  return str;
}

function fixedD(num, len) {
  var s = rightJ(formatNumber(num), len);
  return s;
}

function formatNumber(num) {
  return num.toLocaleString();
}

var hprinted = false;

function printHeader() {
  if (pcnt % 10 == 0) {
    utils.writedata("\r\n");
    utils.writedata("\r\n");
    for (var k in fcstats) {
      utils.writedata(rightJ(k, colw));
    }
    utils.writedata("\r\n");
    for (var k in fcstats) {
      utils.writedata(rightJ("----", colw));
    }
    // utils.writedata('\r\n');
  }
  pcnt++;
}

function print() {
  if (chk()) {
    printHeader();
    utils.writedata("\r\n");
    for (var k in fcstats) {
      utils.writedata(fixedD(fcstats[k], colw));
    }
  }
}
module.exports.print = print;
