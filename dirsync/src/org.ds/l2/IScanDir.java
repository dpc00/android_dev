package org.ds.l2;

import java.io.IOException;

public interface IScanDir {
	void findclose() throws IOException;

	DE findfirst(String fs) throws IOException;

//	DE findItem(String fs) throws IOException;

	DE findnext() throws IOException;
}
