import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.util.Iterator;


public class WindowsDEStream implements DirectoryStream<DE> {
	public DE cde;
	public WindowsScanDir sd;

	public WindowsDEStream(String fspec) {
		try {
			sd = new WindowsScanDir();
			cde = sd.findfirst(fspec);
			while (cde != null && (cde.fname.equals(".") || cde.fname.equals(".."))) {
				cde = sd.findnext();
			}
		} catch (IOException e) {
			System.out.println(e.toString());
			cde = null;
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
}
