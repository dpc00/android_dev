package org.ds.types;

import java.io.File;
import java.util.Arrays;

public class ST {
	public VL vl;
	public String[] pth;

	public ST(VL vl, RT rt) {
		this.vl = vl;
		String re = File.separator;
		re = re.replace("\\", "\\\\");
		this.pth = rt.s.split(re);
	}

	public VL Vl() {
		return this.vl;
	}

	public FP Fp() {
		String rv;
		if (this.pth.length == 1) {
			rv = this.pth[0] + File.separatorChar;
		} else {
			rv = this.pth[0];
			for (int i = 1; i < this.pth.length; i++) {
				rv += File.separatorChar + this.pth[i];
			}
		}
		return new FP(rv);
	}

	public RD Rp() {
		String rv = "";
		if (this.pth.length == 1) {
			rv = File.separatorChar + "";
		} else {
			for (int i = 1; i < this.pth.length; i++) {
				rv += File.separatorChar + this.pth[i];
			}
		}
		return new RD(rv);
	}

	public DItem SDir(RD rd) {
		return new DItem(true, this, rd);
	}

	public DItem SFile(RD rd) {
		return new DItem(false, this, rd);
	}
}
