package org.ds.l3;

import org.ds.l2.DE;

public class OLEntry {
	public OLEntry(OpCode o, DE de) {
		this.opcode = o;
		this.de = de;
	}
	public OpCode opcode;

	public DE de;
}