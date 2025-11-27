var fs = require("fs");
// var jake = require('jake');
var json = require("json");
var utils = require("utils");
var vol = require("vol");
var os = require("os");

function run() {
  if (!process.env.FLASH0) {
    process.env.FLASH0 = __dirname.substring(0, 2);
  }
  // var cfn1 = __dirname + '\\plaunch_flash_' + 'CODE' + '.json';
  var cfn2 = utils.expES("%FLASH0%\\Projects\\tools\\plaunch_flash_CODE0.json");
  var cfn3 = utils.expES("%FLASH0%\\Projects\\tools\\plaunch_hd.json");

  // var splobj1 = json.readConfig(cfn1);
  var splobj2 = json.readConfig(cfn2);
  var splobj3 = json.readConfig(cfn3);

  var ae2 = [];

  function addplines(ps, pre, ae) {
    for (k in ps) {
      if (ps[k].include) {
        var s = pre + k;
        if (s.indexOf(" ") != -1) {
          ae.push('"' + s + '"');
        } else ae.push(s);
      }
    }
  }

  // addplines(splobj1.paths, '%FLASH0%', ae2);

  addplines(splobj2.paths, "%FLASH0%", ae2);
  addplines(splobj3.paths, "C:", ae2);

  var crlf = "\r\n";

  var envstr = "";
  var pstr = "";
  envstr +=
    'for /f "usebackq tokens=1,2 skip=1" %%i in (`wmic VOLUME where drivetype^=2 get label^,driveletter`) do (' +
    crlf;
  envstr += '	if "%%j"=="CODE0" set FLASH0=%%i' + crlf;
  envstr += '	if "%%j"=="CODE1" set FLASH1=%%i' + crlf;
  envstr += '	if "%%j"=="CODE2" set FLASH2=%%i' + crlf;
  envstr += '	if "%%j"=="CODE3" set FLASH3=%%i' + crlf;
  envstr += '	if "%%j"=="CODE4" set FLASH4=%%i' + crlf;
  envstr += '	if "%%j"=="CODE5" set FLASH5=%%i' + crlf;
  envstr += '	if "%%j"=="CODE6" set FLASH6=%%i' + crlf;
  envstr += '	if "%%j"=="CODE7" set FLASH7=%%i' + crlf;
  envstr += ")" + crlf;
  envstr += 'if "%FLASH0%"=="" exit' + crlf;
  envstr += 'if "%FLASH1%"=="" exit' + crlf;
  envstr += "set ARCH=" + os.arch() + crlf;
  // for (k in splobj1.env) {
  // 	envstr += 'set ' + k + '=' + splobj1.env[k] + crlf;
  // }
  for (k in splobj2.env) {
    envstr += "set " + k + "=" + splobj2.env[k] + crlf;
  }
  pstr += "path " + ae2.join(";%path%" + crlf + "path ") + ";%path%" + crlf;

  fs.writeFileSync(
    vol.findDL("CODE0") + "\\.bat\\plaunch.bat",
    "@echo off" + crlf + envstr + pstr + crlf + "@echo on" + crlf + "%*" + crlf
  );
}
module.exports.run = run;

run();
