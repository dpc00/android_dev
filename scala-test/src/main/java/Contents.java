import java.util.HashMap;
import java.nio.file.DirectoryStream;

public class Contents {
	public static boolean option_WDE;
	public HashMap<String, DE> dirs;
	public HashMap<String, DE> files;

	public DirectoryStream<DE> getStream(String s) {
		if(option_WDE) {
			return new WindowsDEStream(s);
		}
		else {
			return new JavaDEStream(s);
		}
	}

	public Contents(String sp1) {
		try (DirectoryStream<DE> des = getStream(sp1)) {
			dirs = new HashMap<>();
			files = new HashMap<>();
			for(DE de: des) {
				if(de.isdir) {
					dirs.put(de.fname, de);
				}
				else if(de.isfile) {
					files.put(de.fname, de);
				}
			}
		}
		catch (Exception e) {
			System.out.println(e.toString());
		}
		
	}
}
