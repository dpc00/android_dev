package org.ds.l3;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.TreeMap;

import org.ds.l2.DE;
import org.ds.l3.CC.Contents;

@SuppressWarnings("serial")
public class OpList extends HashMap<OpCode, ArrayList<DE>> {
	public static OpList NULL = new OpList();
	public int modcnt;

	public OpList() {
	}

	public void add(OpCode oc, DE de) {
		ArrayList<DE> del = get(oc);
		if(del == null) {
			del = new ArrayList<>();
			put(oc, del);
		}
		del.add(de);
	}

	public OpList(Contents sContents, Contents dContents) {
		TreeMap<String, DE> scf = sContents.files;
		TreeMap<String, DE> scd = sContents.dirs;
		TreeMap<String, DE> dcf = dContents.files;
		TreeMap<String, DE> dcd = dContents.dirs;

		if (sContents.blocked || dContents.blocked) return;
		int sc = sContents.dex ? 1 : 0;
		sc |= dContents.dex ? 2 : 0;
		switch (sc) {
			case 0: // neither exist
				break;
			case 1: // new
				add(OpCode.dCrt, null);
				for (DE de1 : scf.values()) {
					add(OpCode.fNew, de1);
				}
				for (DE de1 : scd.values()) {
					add(OpCode.dNew, de1);
				}
				break;
			case 2: // only dest exists
				if (dContents.dex) { // dir deletion
					for (DE de2 : dcd.values()) {
						add(OpCode.dMis, de2);
					}
					for (DE de2 : dcf.values()) {
						add(OpCode.fMis, de2);
					}
					add(OpCode.dDel, null);
				}
				break;
			case 3: // both exist
				for (DE de2 : dcd.values()) { // deleted dirs
					DE de1 = scd.get(de2.fname);
					if (de1 == null || scf.containsKey(de2.fname)) {
						add(OpCode.dMis, de2);
					}
				}
				for (DE de2 : dcf.values()) { // delete deleted files
					DE de1 = scf.get(de2.fname);
					if (de1 == null || scd.containsKey(de2.fname)) {
						add(OpCode.fMis, de2);
					}
				}
				for (DE de1 : scf.values()) { // possibly copy modified/new files
					DE de2 = dcf.get(de1.fname);
					if (de2 == null) { // new file
						add(OpCode.fNew, de1);
					} else if (!de2.isUp2DateWith(de1)) { // modified file
						add(OpCode.fMod, de1);
					}
				}
				for (DE de1 : scd.values()) { // new/existing dirs
					DE de2 = dcd.get(de1.fname);
					if (de2 == null) { // new
						add(OpCode.dNew, de1);
					} else { // existing
						add(OpCode.dExi, de1);
					}
				}
				break;
		}
	}

	public boolean isEmpty() {
		return size() == 0;
	}
}
