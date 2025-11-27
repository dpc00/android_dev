var dirutils = require("dirutils");
var utils = require("utils");
// var jake = require('jake');
var fs = require("fs");
var json = require("json");

function run() {
  var cfn = utils.expES("plaunch_hd.json");
  var splobj = json.readConfig(cfn);

  return dirutils
    .dirsContainingType(
      "C:\\",
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
      [
        "C:\\dell\\drivers",
        "C:\\Program Files (x86)\\Common Files",
        "C:\\Users\\All Users",
        "C:\\Users\\Donald Chitester\\AppData\\Local\\Microsoft\\Windows",
        "C:\\Windows\\assembly",
        "C:\\Windows\\CCM",
        "C:\\Windows\\diagnostics",
        "C:\\Windows\\DriverStore",
        "C:\\Windows\\Installer",
        "C:\\Windows\\Microsoft.NET",
        "C:\\Windows\\SoftwareDistribution",
        "C:\\Windows\\System32\\DriverStore",
        "C:\\Windows\\System32\\en",
        "C:\\Windows\\SysWOW64",
        "C:\\Windows\\winsxs",
      ]
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
module.exports.run = run;
