var cp = require("child_process");
var fs = require("fs");
var path = require("path");
var utils = require("utils");

function readConfig(fn) {
  var data = fs.readFileSync(fn, "utf8");
  if (data) {
    utils.log(fn + " loaded.");
    // if (typeof stripJSONComments == 'undefined') {
    // 	var stripJSONComments = require('strip-json-comments');
    // }
    var rv = JSON.parse(data);
    if (!rv) {
      utils.log("error parsing " + fn);
    }
    return rv;
  }
}
module.exports.readConfig = readConfig;

function writeConfig(obj, fn) {
  var obj_s = JSON.stringify(obj, null, "\t");
  fs.writeFileSync(fn, obj_s, "ascii");
  utils.log(fn + " written.");
}
module.exports.writeConfig = writeConfig;

function writePlaunchJSON(obj, fn, finc) {
  var il = 0;
  function fmt(obj) {
    var s1 = "";
    if (typeof obj == "object") {
      if (Array.isArray(obj)) s1 += '["' + obj.join('","') + '"]';
      else s1 += inbraces(obj);
    } else {
      if (typeof obj == "boolean") s1 += obj ? "true" : "false";
      else {
        if (typeof obj == "string") {
          var s0 = obj.toString();
          s0 = s0.replace(/\\/gi, "\\\\");
          s1 += '"' + s0 + '"';
        } else s1 += JSON.stringify(obj, null, "\t");
      }
    }
    return s1;
  }

  function ilts(n) {
    var s = "";
    for (var i = 0; i < n; i++) s += "\t";
    return s;
  }

  function inbraces(obj) {
    il++;
    var s = "{\r\n" + ilts(il + 1) + fmt2(obj) + ilts(il) + "}";
    il--;
    return s;
  }

  function fmt2(obj) {
    var first = true;
    var s = "";
    for (k in obj) {
      if (!first) {
        s += ",\r\n" + ilts(il + 1);
      } else first = false;
      var s0 = k.toString().replace(/\\/gi, "\\\\");
      s0 = '"' + s0 + '": ';
      s += s0 + fmt(obj[k]);
    }
    s += "\r\n";
    return s;
  }
  var obj_s = fmt(obj);
  fs.writeFileSync(fn, obj_s, "ascii");
  utils.log(fn + " written.");
}
module.exports.writePlaunchJSON = writePlaunchJSON;

function sortJSONFile(fn) {
  var jsf = readConfig(fn);
  if (typeof sds == "undefined") {
    var sds = require("smart-deep-sort");
  }
  var sjsf = sds(jsf);
  writeConfig(sjsf, fn + ".sorted");
}
module.exports.sortJSONFile = sortJSONFile;
