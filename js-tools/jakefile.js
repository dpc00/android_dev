/// <ref path="typings/main.d.ts"/>

var cf = require('copy_flash');
var Dos4 = require('dos4');
var dirutils = require('dirutils');
var GitRepo = require('gitrepo').GitRepo;
var jake = require('jake');
var utils = require('utils');

function fl(spec) {
	var list = new jake.FileList();
	list.include(spec);
	return list.toArray();
}

function pause() {
	return new Promise(
		function(resolve, reject) {
			utils.writedata('press enter...');
			var buf = process.stdin.read(1);
			resolve(buf);
		}
	);
}

desc('runs all backups');
task('backups', ['bat:backup', 'git:backup'],
	function() {
		var tn = this.fullName;
		jake.logger.log("'" + tn + "' starting");
		jake.logger.log("'" + tn + "' done.");
		complete();
	}, true
);

namespace('bat', function() {
	desc('touch bat files');
	task('touch', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");
			dirutils.touchBats().then(function() {
				jake.logger.log("'" + tn + "' done.");
				complete();
			});
		}, true
	);
	desc('runs bat backup');
	task('backup', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");
			var d1 = utils.expES('%FLASH0%\\Projects\\tools\\.bat');
			var d2 = utils.expES('%FLASH0%\\.bat');
			var d3 = utils.expES('%FLASH0%\\Projects\\tools\\.lnk');
			var d4 = utils.expES('%FLASH0%\\.lnk');
			directory(d1).invoke();
			directory(d3).invoke();
			cf.dirCopy(d1, d2).then(
				function() {
					return cf.dirCopy(d2, d1);
				}
			).then(
				function() {
					return cf.dirCopy(d3, d4);
				}
			).then(
				function() {
					return cf.dirCopy(d4, d3);
				}
			).then(
				function() {
					jake.logger.log("'" + tn + "' done.");
					complete();
				}
			);
		}, true
	);
});

task('build', ['compile'],
	function() {
		var tn = this.fullName;
		jake.logger.log("'" + tn + "' starting");
		jake.logger.log("'" + tn + "' done.");
	}, false
);

task('compile', ['frege:compile', 'java:compile', 'typescript:compile'],
	function() {
		var tn = this.fullName;
		jake.logger.log("'" + tn + "' starting");
		jake.logger.log("'" + tn + "' done.");
	}, false
);

//.....
namespace('cpl', function() {
	desc('makes plaunch_hd.json');
	task('hd', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");
			require('cpl_hd').run().then(function() {
				jake.logger.log("'" + tn + "' done.");
				complete();
			});
		}, true
	);
	desc('makes plaunch_flash_????????.json');
	task('flash', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");
			require('cpl_flash').run().then(function() {
				jake.logger.log("'" + tn + "' done.");
				complete();
			});
		}, true
	);
	desc('makes plaunch.bat');
	task('bat', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");
			require('cpl_bat').run();
			jake.logger.log("'" + tn + "' done.");
			complete();
		}, true
	);
});

task('default', [],
	function() {
		var tn = this.fullName;
		jake.logger.log("'" + tn + "' starting");
		// utils.showenv();
		jake.logger.log("'" + tn + "' done.");
	}, false
);

namespace('flash-backup', function() {
	desc('runs javascript full flash backup');
	task('node-full', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");
			return cf.fcopy1().then(
				function() {
					jake.logger.log("'" + tn + "' done.");
					return pause().then(
						function() {
							complete();
						}
					);
				}
			);
		}, true
	);
	desc('runs javascript partial flash backup');
	task('node-partial', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");
			return cf.fcopy2().then(
				function() {
					jake.logger.log("'" + tn + "' done.");
					return pause().then(
						function() {
							complete();
						}
					);
				}
			);
		}, true
	);
	desc('runs dirsyncpro');
	task('dirsyncpro', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");
			return cf.dsPro().then(function() {
				jake.logger.log("'" + tn + "' done.");
				complete();
			});
		}, true
	);
});

namespace('frege', function() {
	desc('compile frege files');
	task('compile', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");

			function compile(srcfile) {
				return new Dos4({
					cmd: 'java.exe',
					args: ['-Dfrege.javac=\\Programs\\jre1.8.0_73\\bin\\java.exe -jar ../ecj-4.5.1.jar -7 -encoding UTF-8', '-jar', '../frege-3.23.422-ga05a487.jar', '-d', 'out', srcfile],
					collect: false,
					echo: false,
					print: true
				});
			}
			var v1 = fl('src/**/*.fr');
			var p1 = Promise.resolve();
			v1.forEach(function(d) {
				p1 = p1.then(function() {
					return compile(d);
				});
			});
			return p1.then(
				function() {
					jake.logger.log("'" + tn + "' done.");
					complete();
				}
			);
		}, true
	);
});

namespace('git', function() {
	function getRepos() {
		return utils.prjList.map(function(prj) {
			return new GitRepo({
				wt: utils.prjDir(prj),
				gd: utils.gitDir(prj)
			});
		});
	}
	desc('runs git backup');
	task('backup', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");
			var repos = getRepos();
			var p1 = Promise.resolve();
			repos.forEach(
				function(gr) {
					p1 = p1.then(
						function() {
							return gr.backup();
						}
					);
				}
			);
			return p1.then(
				function() {
					jake.logger.log("'" + tn + "' done.");
					return pause().then(
						function() {
							complete();
						}
					);
				}
			);
		}, true
	);
	desc('runs git status');
	task('status', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");
			var repos = getRepos();
			var p1 = Promise.resolve();
			repos.forEach(
				function(gr) {
					p1 = p1.then(
						function() {
							return gr.status();
						}
					);
				}
			);
			return p1.then(
				function() {
					jake.logger.log("'" + tn + "' done.");
					return pause().then(
						function() {
							complete();
						}
					);
				}
			);
		}, true
	);
});

namespace('java', function() {
	// var ant = require('ant');
	var utils = require('utils');
	desc('compile java files');
	task('compile', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");

			function javacompile(srcfile) {
				return new Dos4({
					cmd: 'java.exe',
					args: ['-jar', '../ecj-4.5.1.jar', '-cp', '../frege-3.23.422-ga05a487.jar', '-encoding', 'UTF-8', '-d', 'out', '-8', '-g', '-verbose', srcfile],
					collect: false,
					echo: true,
					print: true
				});
			}

			function javabuild(sd, dd) {
				return new Promise(function(resolve, reject) {
					ant.exec({
							property: {
								'@name': "build.compiler",
								'@value': "org.eclipse.jdt.core.JDTCompilerAdapter",
							},
							// property: {
							// 	'@name':'prop.message',
							// 	'@value': 'must be defined, preferably in config/${config.filename} (details at javaranch.com/props)'
							// },
							// fail: { 
							// 	'@message': 'db.schema ${prop.message}',
							// 	'@unless': 'db.schema'
							// },
							mkdir: {
								'@dir': dd
							},
							javac: {
								'@source': '1.8',
								'@target': '1.8',
								// '@classpath': '',
								'@debug': 'on',
								'@srcdir': sd,
								'@destdir': dd,
								'@verbose': 'false',
								'@includeantruntime': false,
								'compilerclasspath': {
									'pathelement': {
										'@path': utils.expES('%FLASH0%\\Projects\\lib\\ecj-4.5.1.jar')
									}
								}
							}
						}, [],
						(err, stdout, stderr) => {
							utils.eo(stdout, stderr);
							if (err) reject(err);
							else resolve();
						}
					);
				});
			}
			var p1 = Promise.resolve();
			utils.prjList.forEach(
				function(prj) {
					var sd = utils.prjDir(prj) + '\\src';
					var dd = utils.prjDir(prj) + '\\classes';
					p1 = p1.then(
						function() {
							return javabuild(sd, dd).catch(
								function(err) {
									console.log(err.message);
								}
							);
						}
					);
				}
			);
			p1 = p1.then(
				function() {
					jake.logger.log("'" + tn + "' done.");
					complete();
				}
			);
			return p1;
		}, true
	);
});

namespace('modules', function() {
	desc('cleans out node_modules');
	task('cleandev', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");

			function npmcmd(cargs) {
				return new Dos4({
					cmd: 'npm',
					args: cargs,
					collect: false,
					echo: true,
					print: true
				});
			}
			var v1 = fl('node_modules/*');
			var v2 = v1.map(function(f) {
				return path.basename(f);
			});
			npmcmd(['uninstall', '--save-dev'].concat(v2)).then(
				function() {
					var pa = v2.map(function(f) {
						return new Dos4({
							cmd: 'cmd.exe',
							args: ['/c', 'rmdir', '/S', '/Q', 'node_modules\\', f],
							collect: false,
							echo: true,
							print: true
						});
					});
					return Promise.all(pa).then(function() {
						jake.logger.log("'" + tn + "' done.");
						complete();
					});
				}
			);
		}, true
	);
});

namespace('npm', function() {
	var utils = require('utils');
	desc('runs npm dedupe');
	task('dedupe', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");
			return new Dos4({
				cmd: 'npm.cmd',
				args: ['dedupe', '-g'],
				print: true,
				collect: false,
				echo: true
			}).then(
				function() {
					jake.logger.log("'" + tn + "' done.");
					complete();
				}
			);
		}, true
	);
});

task('sublimetext', [],
	function() {
		var tn = this.fullName;
		jake.logger.log("'" + tn + "' starting");
		cf.sublimeText();
		jake.logger.log("'" + tn + "' done.");
	}, false
);

namespace('typescript', function() {
	var utils = require('utils');
	desc('transpiles TypeScript files');
	task('compile', [],
		function() {
			var tn = this.fullName;
			jake.logger.log("'" + tn + "' starting");
			return new Dos4({
				cmd: 'tsc.cmd',
				args: ['-p', '.'],
				echo: true,
				print: true
			}).then(function() {
				jake.logger.log("'" + tn + "' done.");
				complete();
			});
		}, true
	);
});