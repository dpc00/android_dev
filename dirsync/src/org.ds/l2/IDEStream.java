package org.ds.l2;

import java.nio.file.DirectoryStream;

public interface IDEStream extends DirectoryStream<DE> {
	int dError();
	Exception dException();
}
