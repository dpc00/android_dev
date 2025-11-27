package org.ds.l4;

import java.util.concurrent.ConcurrentHashMap;
import java.util.function.BiConsumer;

import org.ds.l3.CC;
import org.ds.l3.CC.Contents;
import org.ds.types.DItem;
import org.ds.types.VL;

public class CHM {
	public static ConcurrentHashMap<DItem, CC.Contents> hm = new ConcurrentHashMap<>();
	public static long misses, hits;

	public CC cc;
	
	public CHM(CC cc) {
		this.cc = cc;
	}
	
	public Contents get(DItem key) {
		// TODO Auto-generated method stub
		CC.Contents c = hm.get(key);
		if(c == null || c.utime > c.ftime) {
			misses++;
			c = new Contents((DItem)key);
			hm.put((DItem)key, c);
			cc.dirsread.setV((Long) cc.dirsread.getV() + 1L);
			cc.filesread.setV((Long) cc.filesread.getV() + (long) c.files.size());
			cc.dirscached.setV((Long)cc.dirscached.getV() + 1);
		} else {
			hits++;
		}
		return c;
	}

	public Contents get2(DItem key) {
		// TODO Auto-generated method stub
		misses++;
		CC.Contents c = new Contents((DItem)key);
		cc.dirsread.setV((Long) cc.dirsread.getV() + 1L);
		cc.filesread.setV((Long) cc.filesread.getV() + (long) c.files.size());
		cc.dirscached.setV((Long)cc.dirscached.getV() + 1);
		return c;
	}
	
	public CC.Contents remove(DItem key) {
		cc.dirscached.setV((Long)cc.dirscached.getV() - 1L);
		return hm.remove(key);
	}

	public void clear() {
		VL s1 = cc.st.Vl();
		hm.forEach(new BiConsumer<DItem, CC.Contents>() {
			public void accept(DItem k, CC.Contents c) {
				VL s2 = k.Vl();
				if(s1.equals(s2)) {
					hm.remove(k);
				}
			}
		});
	}
}
