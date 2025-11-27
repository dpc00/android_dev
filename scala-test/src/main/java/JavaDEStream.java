import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Iterator;


public class JavaDEStream implements DirectoryStream<DE> {
	public static FileSystem fs = FileSystems.getDefault();
	public DirectoryStream<Path> ds;
	public Iterator<Path> dsi;
	public DE cde;

	public JavaDEStream(String fspec) {
		try {
			ds = Files.newDirectoryStream(Paths.get(fspec));
			dsi = ds.iterator();
			getNext();
		}
		catch(IOException e) {
			System.out.println(e.toString());
			cde = null;
		}
	}

	public void close() {
		if(ds!=null) {
			try {
				ds.close();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				System.out.println(e.toString());
			}
			ds = null;
		}
		cde = null;
	}

	public Iterator<DE> iterator() {
		return new JDES_Iterator();
	}

	public class JDES_Iterator implements Iterator<DE> {
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
		if(dsi.hasNext()) {
			cde = new DE(dsi.next());
			while(cde!=null && cde.fname.equals(".") || cde.fname.equals("..")) {
				if(dsi.hasNext()) {
					cde = new DE(dsi.next());
				}
				else cde = null;
			}
		}
		else cde = null;
	}
}