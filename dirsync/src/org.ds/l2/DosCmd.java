package org.ds.l2;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

import org.ds.l3.Failure;
import org.ds.l3.Success;
import org.ds.l3.Try;

public class DosCmd {
	public static Try<DosCmd.RetV, DosCmd.RetV> exec(String s) {
		BufferedReader br1 = null;
		BufferedReader br2 = null;
		InputStreamReader isr1 = null;
		InputStreamReader isr2 = null;
		Process p = null;
		ArrayList<String> als1 = new ArrayList<>();
		ArrayList<String> als2 = new ArrayList<>();
		try {
			p = Runtime.getRuntime().exec("cmd /c " + s);
			isr1 = new InputStreamReader(p.getInputStream());
			isr2 = new InputStreamReader(p.getErrorStream());
			br1 = new BufferedReader(isr1);
			br2 = new BufferedReader(isr2);
			String line;
			while ((line = br1.readLine()) != null) {
				als1.add(line.trim());
			}
			while ((line = br2.readLine()) != null) {
				als2.add(line.trim());
			}
			if (p.exitValue() == 0) {
				return new Success<>(new RetV(als1, als2, 0, null));
			}
			return new Failure<>(new RetV(als1, als2, p.exitValue(), null));
		} catch (IOException e) {
			return new Failure<>(new RetV(als1, als2, -1, e));
		} finally {
			// close the streams using close method
			try {
				if (br1 != null) {
					br1.close();
				}
				if (isr1 != null) {
					isr1.close();
				}
				if (br2 != null) {
					br2.close();
				}
				if (isr2 != null) {
					isr2.close();
				}
			} catch (IOException ioe) {
				System.out.println("Error while closing something: " + ioe);
			}
		}
	}

	public static class RetV {
		RetV(ArrayList<String> al1, ArrayList<String> al2, int ec, IOException ioe) {
			this.stdout = al1;
			this.stderr = al2;
			this.ec = ec;
			this.ioe = ioe;
		}
		public ArrayList<String> stdout;
		public ArrayList<String> stderr;
		public int ec;

		public IOException ioe;
	}
}
