import java.util.HashMap;
import java.util.ArrayList;

public class OpLists {
	ArrayList<DE> cDirs;
	ArrayList<DE> cFiles;
	ArrayList<DE> dDirs;
	ArrayList<DE> dFiles;
	HashMap<String, DE> ocd;
	HashMap<String, DE> ocf;
	HashMap<String, DE> scd;
	HashMap<String, DE> scf;

	public OpLists(Contents sContents, Contents dContents) {
		ocd = dContents.dirs;
		ocf = dContents.files;
		scd = sContents.dirs;
		scf = sContents.files;

		for (String si: scf.keySet()) {
			if(!ocf.containsKey(si) || !scf.get(si).equals(ocf.get(si))) {
				if(cFiles==null) cFiles = new ArrayList<DE>();
				cFiles.add(scf.get(si));
			}
		}

		for(String di: ocf.keySet()) {
			if(!scf.containsKey(di) || scd.containsKey(di)) {
				if(dFiles==null) dFiles = new ArrayList<DE>();
				dFiles.add(ocf.get(di));
			}
		}

		for(String si: scd.keySet()) {
			if(cDirs==null) cDirs = new ArrayList<DE>();
			cDirs.add(scd.get(si));
		}
		
		for(String di: ocd.keySet()) {
			if(!scd.containsKey(di) || scf.containsKey(di)) {
				if(dDirs==null) dDirs = new ArrayList<DE>();
				dDirs.add(ocd.get(di));
			}
		}
	}
}