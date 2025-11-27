package org.ds.cn;

import java.io.Closeable;

public interface IChangeNotifier extends Closeable {
	void close();
	void start();
}
