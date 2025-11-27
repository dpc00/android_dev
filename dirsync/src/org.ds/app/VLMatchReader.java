package org.ds.app;

import org.ds.types.RT;
import org.ds.types.VL;

import java.util.ArrayList;
import java.util.function.Consumer;
import java.util.function.Predicate;

public class VLMatchReader extends ParamReader {

	@SafeVarargs
	public VLMatchReader(Predicate<VL>... vls) {
		this.rts = new ArrayList<>();
		iterFS(
			new Consumer<FSData>() {
				public void accept(FSData fsd) {
					RtData rtd = new RtData();
					rtd.dl = fsd.drv;
					rtd.vl = fsd.lbl;
					rtd.sn = fsd.vsn;
					rtd.tot = fsd.tot;
					rtd.free = fsd.free;
					rtd.rt = new RT(rtd.dl + "\\");
					if (vls[0].test(rtd.vl)) {
						VLMatchReader.this.rts.add(0, rtd);
					} else
						for (int i = 1; i < vls.length; i++) {
							if (vls[i].test(rtd.vl)) {
								VLMatchReader.this.rts.add(rtd);
							}
						}
				}
			}
		);
	}
}
