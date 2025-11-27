package org.ds.ui;

import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;
import java.util.stream.Collectors;

import org.ds.app.DirSyncApp;

import javafx.application.Platform;
import javafx.scene.control.TextArea;

public class TextWrap extends PrintStream {
	public static TextWrap it = new TextWrap();
	private static String delims = "\\/,;-%&$![]{}|<>? ";

	private TextWrap() {
		super(System.out);
	}

	public static List<String> minNumLinesWrap(String text, int lw, int ts) {
		ArrayList<String> sa = new ArrayList<>();
		String cl = null;
		StringTokenizer tokenizer = new StringTokenizer(text, delims, true);
		int lw2 = lw;
		while (tokenizer.hasMoreTokens()) {
			String tok = tokenizer.nextToken();
			if (((tok.length() + ((cl != null) ? cl.length() : 0)) >= lw2 - 1)
					&& !(tok.length() == 1 && (delims.contains(tok.substring(0, 1))) && !tok.equals(" "))) {
				if (cl != null) {
					sa.add(cl.trim());
					lw2 = lw - ts;
				}
				cl = tok.trim();
			} else {
				cl = (cl == null) ? tok : cl + tok;
			}
		}
		if (((cl != null) ? cl.length() : 0) > 0)
			sa.add(cl);
		return sa;
	}

	public void print(String s1) {
		List<String> sa = minNumLinesWrap(s1, 80, 12);
		final String s2 = sa.stream().collect(Collectors.joining("\n\t"));
		taprint(s2);
	}

	public void println(String s) {
		if (s == null)
			s = "";
		print(s + "\n");
		// Console.println()
	}

	public void taprint(String s1) {
		if(DirSyncApp.it == null) {
			System.out.print(s1);
			return;
		}
		TextArea tae = DirSyncApp.it.taEvents;
		if (tae != null) {
			try {
				Platform.runLater(() -> {
					int caretPosition = tae.caretPositionProperty().get();
					boolean atBottom = caretPosition == tae.getLength();
					tae.appendText(s1);
					int cl = tae.getLength();
					final int dl = 4096;
					if(cl > dl) {
						tae.setText(tae.getText((cl-dl), cl));
						caretPosition -= (cl-dl);
						if(caretPosition<0) caretPosition = 0;
					}
					if (!atBottom) tae.positionCaret(caretPosition);
				});
			} catch (Exception e) {
			}
		}
	}

//	public void write(int i) {
//		if(DirSyncApp.it == null) {
//			System.out.write(new Integer(i).toString());
//			return;
//		}
//		TextArea tae = DirSyncApp.it.taEvents;
//		if (tae != null) {
//			try {
//				Platform.runLater(() -> {
//					int caretPosition = tae.caretPositionProperty().get();
//					boolean atBottom = caretPosition == tae.getLength();
//					tae.appendText(new Integer(i).toString());
//					if (!atBottom)
//						tae.positionCaret(caretPosition);
//				});
//			} catch (Exception e) {
//			}
//		}
//	}

	public void taprintln(String s) {
		if (s == null)
			s = "";
		taprint(s + "\n");
	}
}