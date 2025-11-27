package org.ds.l4;

import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.TreeSet;
import java.util.stream.Collectors;

import org.ds.app.RtData;
import org.ds.cn.ChangeRecord;
import org.ds.types.RT;
import org.ds.types.ST;
import org.ds.ui.TextWrap;

public class DSList {
	public ChangeRecord ar;
	public DSSI s;
	public TreeSet<DSTI> d = new TreeSet<>();

	public void clearCCs() {
		this.s.cc.clear();
		for (DSTI te : this.d) {
			te.cc.clear();
		}
	}

	public DSList build2(ArrayList<RtData> parms) {
		RtData rtd1 = parms.get(0);
		String sp = Paths.get(rtd1.rt.s).toAbsolutePath().toString();
		ST st = new ST(rtd1.vl, new RT(sp));
		// ar = new ChangeRecord(rt);

		DSSI dssi = new DSSI(st, null, this.ar);
		// ar.getRoot().setValue(rt);
		// ar.setShowRoot(false);
		// ar.cnl_cnt = -1;
		// ar.refreshTreeView();
		this.s = dssi;


		this.d.clear();
		if (parms.size() > 1) {
			for (int ii = 1; ii < parms.size(); ii++) {
				RtData rtd2 = parms.get(ii);
				String s = rtd2.rt.s;
				String dp = Paths.get(s).toAbsolutePath().toString();
				ST st2 = new ST(rtd2.vl, new RT(dp));
				DSTI dsti = new DSTI(st2, null);
				this.d.add(dsti);
				dsti.ds = new DirSyncer(dssi, dsti, this.ar);
				TextWrap.it.taprintln("\t-\t" + dp);
			}
		}
		return this;
	}

	public DSList build1(ArrayList<RtData> parms) {
		RtData rtd1 = parms.get(0);
		String sp = Paths.get(rtd1.rt.s).toAbsolutePath().toString();
		ST st = new ST(rtd1.vl, new RT(sp));
		this.ar = new ChangeRecord(st);

		DSSI dssi = new DSSI(st, null, this.ar);
		this.ar.getRoot().setValue(st.Fp());
		this.ar.setShowRoot(false);
		this.ar.cnl_cnt = -1;
		this.ar.refreshTreeView();
		this.s = dssi;

		@SuppressWarnings("unchecked")
		ArrayList<RtData> parms2 = (ArrayList<RtData>) parms.clone();
		parms2.remove(0);

		this.d.clear();
		if (!parms2.isEmpty()) {
			for (int ii = 0; ii < parms2.size(); ii++) {
				RtData rtd2 = parms2.get(ii);
				String s = rtd2.rt.s;
				String dp = Paths.get(s).toAbsolutePath().toString();
				RT rt2 = new RT(dp);
				ST st2 = new ST(rtd2.vl, rt2);
				DSTI dsti = new DSTI(st2, null);
				this.d.add(dsti);
				dsti.ds = new DirSyncer(dssi, dsti, this.ar);
				TextWrap.it.taprintln("\t-\t" + dp);
			}
		}
		return this;
	}

	public List<DSTI> getD() {
		return this.d.stream().collect(Collectors.toList());
	}
}
