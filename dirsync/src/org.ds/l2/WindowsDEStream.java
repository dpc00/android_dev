package org.ds.l2;

import java.io.IOException;
import java.nio.file.*;
import java.util.Iterator;


public class WindowsDEStream implements IDEStream {
	public DE cde;
	public WindowsScanDir sd;
	private Exception dx;

	public WindowsDEStream(String fspec) throws IOException {
		try {
			sd = new WindowsScanDir();
			cde = sd.findfirst(fspec);
			while (cde != null && (cde.fname.equals(".") || cde.fname.equals(".."))) {
				cde = sd.findnext();
			}
		} catch (AccessDeniedException | NoSuchFileException | NotDirectoryException e) {
			this.dx = e;
			throw e;
		}
		catch (FileSystemException e) {
			System.out.println(e.toString());
			this.dx = e;
			throw e;
		} catch (IOException e) {
			System.out.println(e.toString());
			this.dx = e;
			cde = null;
			throw e;
		}
	}

	public void close() {
		// System.out.println("DEStream close()");
		sd.findclose();
		sd = null;
	}

	public Iterator<DE> iterator() {
		return new DES_Iterator();
	}

	public class DES_Iterator implements Iterator<DE> {
		public boolean hasNext() {
			return cde != null;
		}

		public DE next() {
			DE rde = cde;
			getNext();
			return rde;
		}

	}

	public void getNext() {
		try {
			cde = sd.findnext();
			while (cde != null && (cde.fname.equals(".") || cde.fname.equals(".."))) {
				cde = sd.findnext();
			}
		} catch (IOException e) {
			System.out.println(e.toString());
			cde = null;
		}
	}
	public Exception dException() {
		return this.dx;
	}
	public int dError() {
		return 0;
	}

}
