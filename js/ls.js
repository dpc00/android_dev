const { spawn } = require("child_process");

// const child = spawn('pwd');
const child = spawn("ls", ["-Rla"]);

child.on("exit", function (code, signal) {
  console.log(
    "child process exited with " + `code ${code} and signal ${signal}`
  );
});

child.stdout.on("data", (data) => {
  console.log(`child stdout: ${data}`);
});

child.stderr.on("data", (data) => {
  console.error(`child stderr: ${data}`);
});
