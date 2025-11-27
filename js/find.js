const { spawn } = require("child_process");

// const child = spawn('pwd');
const p1 = new Promise((res, rej) => {
  var txt = "";
  const child = spawn("rclone", ["lsjson", ".", "--files-only","--recursive"]);

  child.on("error", function (err) {
    rej(err);
  });

  child.on("exit", function (code, signal) {
    console.log(
      "child process exited with " + `code ${code} and signal ${signal}`
    );
    js = JSON.parse(txt);
    res(js);
  });

  child.stdout.on("data", (data) => {
    // console.log(`child stdout: ${data}`);
    txt += data;
  });

  child.stderr.on("data", (data) => {
    console.error(`child stderr: ${data}`);
  });
});

(async ()=>{
   console.log("---");
   var js = await p1;
   console.log(js);
})();

console.log('done.')