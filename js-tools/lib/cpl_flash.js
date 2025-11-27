var dirutils = require("dirutils");
var fs = require("fs");
var json = require("json");
var utils = require("utils");
var vol = require("vol");

function doFlashDrive(vl) {
  var cfn = vol.findDL(vl) + "\\Projects\\tools\\plaunch_flash_" + vl + ".json";
  var splobj = {};
  try {
    splobj = json.readConfig(cfn);
  } catch (e) {
    utils.errlog(e);
  }
  for (var k in splobj.paths) {
    if (!splobj.paths[k].include) {
      delete splobj.paths[k];
    }
  }
  return dirutils
    .dirsContainingType(
      vol.findDL(vl) + "\\",
      [
        ".acm",
        ".ax",
        ".bat",
        ".cmd",
        ".com",
        ".cpl",
        ".dll",
        ".drv",
        ".efi",
        ".exe",
        ".js",
        ".jse",
        ".msc",
        ".mui",
        ".ocx",
        ".scr",
        ".sys",
        ".tsp",
        ".vbe",
        ".vbs",
        ".wsf",
        ".wsh",
      ],
      false,
      [vol.findDL(vl) + "\\" + "FQZGJQYA"]
    )
    .then(function (ae1) {
      var ae2 = ae1.sort(function (a, b) {
        return a.path.toLowerCase().localeCompare(b.path.toLowerCase());
      });
      ae2.forEach(function (a) {
        if (a.path.substring(1, 2) == ":") {
          a.path = a.path.substring(2);
        }
      });
      ae2.forEach(function (pd) {
        // add new ones
        var ni = function () {
          if (typeof splobj.paths[pd.path] == "undefined") return pd.include;
          else return splobj.paths[pd.path].include;
        };
        splobj.paths[pd.path] = {
          include: ni(),
          //			,'files': pd.files
        };
      });
      json.writePlaunchJSON(splobj, cfn, true);
    });
}
module.exports.doFlashDrive = doFlashDrive;

function run() {
  // doFlashDrive('CODE');
  return doFlashDrive("CODE0");
}
module.exports.run = run;
