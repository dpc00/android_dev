package org.ds.l2;

import java.io.IOException;
import java.nio.file.AccessDeniedException;
import java.nio.file.DirectoryStream;
import java.nio.file.FileSystem;
import java.nio.file.FileSystemException;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.NotDirectoryException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Iterator;

//import sun.nio.fs.WindowsPath.WindowsPathWithAttributes;


public class JavaDEStream implements IDEStream {

	public static FileSystem fs = FileSystems.getDefault();

	public JavaDEStream(String fspec) throws IOException {
		try {
			this.ds = Files.newDirectoryStream(Paths.get(fspec));
			this.dsi = this.ds.iterator();
			getNext();
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
			throw e;
		}
	}

	private DirectoryStream<Path> ds;
	private Iterator<Path> dsi;
	DE cde;

	private int derr;
	private Exception dx;

	public void close() {
		if (this.ds != null) {
			try {
				this.ds.close();
			} catch (IOException e) {
				System.out.println(e.toString());
				this.dx = e;
			}
			this.ds = null;
		}
		this.cde = null;
	}

	public int dError() {
		return this.derr;
	}

	public Exception dException() {
		return this.dx;
	}

	public Iterator<DE> iterator() {
		return new JDES_Iterator();
	}

	void getNext() {
		if (this.dsi.hasNext()) {
			this.cde = DE.fromPath(this.dsi.next());
			while (this.cde != null && (this.cde.fname.equals(".") || this.cde.fname.equals(".."))) {
				if (this.dsi.hasNext()) {
					this.cde = DE.fromPath(this.dsi.next());
				} else
					this.cde = null;
			}
		} else
			this.cde = null;
	}

	class JDES_Iterator implements Iterator<DE> {
		public boolean hasNext() {
			return JavaDEStream.this.cde != null;
		}

		public DE next() {
			DE rde = JavaDEStream.this.cde;
			getNext();
			return rde;
		}
	}
}