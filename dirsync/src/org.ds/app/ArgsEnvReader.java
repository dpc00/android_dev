package org.ds.app;

import java.util.ArrayList;
import java.util.function.Consumer;

import org.ds.types.DL;
import org.ds.types.RT;

public class ArgsEnvReader extends ParamReader {

	public ArgsEnvReader(ArrayList<String> args) {
		this.rts = new ArrayList<>();
		for (String s : args) {
			RtData rtd = new RtData();
			this.rts.add(rtd);
			rtd.rt = new RT(s);
			rtd.dl = new DL(s.substring(0, 2));
			iterFS(new Consumer<FSData>() {
				public void accept(FSData fsd) {
					if (fsd.drv.equals(rtd.dl)) {
						rtd.vl = fsd.lbl;
						rtd.sn = fsd.vsn;
						rtd.tot = fsd.tot;
						rtd.free = fsd.free;
					}
				}
			});
		}
	}
}
