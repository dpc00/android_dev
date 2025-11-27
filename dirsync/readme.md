# DirSyncApp

This project is an attempt at a translation to java of a dir synchronization program written in python (py-test repo) which itself was an attempt to translate from javascript (tools repo).

The operative code itself is a basically simple directory tree walk implementation.

It used BridJ for windows directory calls for speed.  It used BridJ for windows file notification services also.  The code turned out quite good/interesting but was a difficult exercise and there are no plans to try to repeat the error.  Now it is using java only with special tunings:

	change notifier: ExtendedWatchEventModifier.FILE_TREE
	directory reader: sun.nio.fs.WindowsPath.WindowsPathWithAttributes

The UI uses javafx.

It is built using ... several IDEs

The learning process and complexity of using javafx, and BridJ has been way too time-consuming.  

