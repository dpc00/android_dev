package org.ds.event;

import javafx.event.Event;
import javafx.event.EventType;

public class DSEventType {
	private static final EventType<AEvent> DIRSYNC = new EventType<>(Event.ANY, "DIRSYNC");

	public static final EventType<AEvent> ACTION = new EventType<>(DSEventType.DIRSYNC, "ACTION");
	public static final EventType<AEvent> AREV = new EventType<>(DSEventType.DIRSYNC, "AREV");
	public static final EventType<AEvent> CHANGE = new EventType<>(DSEventType.DIRSYNC, "CHANGE");
	public static final EventType<AEvent> CN = new EventType<>(DSEventType.DIRSYNC, "CN");
	public static final EventType<AEvent> ERROR = new EventType<>(DSEventType.DIRSYNC, "ERROR");

	public static final EventType<AEvent> CNTSSCAN = new EventType<>(DSEventType.ACTION, "CNTSSCAN");
	private static final EventType<AEvent> BEGINSCAN = new EventType<>(DSEventType.ACTION, "BEGINSCAN");
	// public static final EventType<AEvent> SCANNING = new
	// EventType<AEvent>(DSEventType.ACTION, "BEGINSCAN");
	public static final EventType<AEvent> ENDSCAN = new EventType<>(DSEventType.ACTION, "ENDSCAN");

	public static final EventType<AEvent> SCANNING = new EventType<>(DSEventType.BEGINSCAN, "SCANNING");
	public static final EventType<AEvent> SCANNING_FC = new EventType<>(DSEventType.SCANNING, "SCANNING_FC");

	private static final EventType<AEvent> SKIPPING = new EventType<>(DSEventType.BEGINSCAN, "SKIPPING");
	public static final EventType<AEvent> SKIPPING_FC = new EventType<>(DSEventType.SKIPPING, "SKIPPING_FC");
	public static final EventType<AEvent> SKIPPING_DC = new EventType<>(DSEventType.SKIPPING, "SKIPPING_DC");
	public static final EventType<AEvent> SKIPPING_SDC = new EventType<>(DSEventType.SKIPPING, "SKIPPING_SDC");
	public static final EventType<AEvent> SKIPPING_SFC = new EventType<>(DSEventType.SKIPPING, "SKIPPING_SFC");

	public static final EventType<AEvent> CREATEDIR = new EventType<>(DSEventType.CHANGE, "CREATEDIR");
	public static final EventType<AEvent> COPYFILE = new EventType<>(DSEventType.CHANGE, "COPYFILE");
	public static final EventType<AEvent> DELETEFILE = new EventType<>(DSEventType.CHANGE, "DELETEFILE");
	public static final EventType<AEvent> REMOVEDIR = new EventType<>(DSEventType.CHANGE, "REMOVEDIR");

	public static final EventType<AEvent> CNADD = new EventType<>(DSEventType.CN, "CNADD");
	public static final EventType<AEvent> CNREM = new EventType<>(DSEventType.CN, "CNREM");
	public static final EventType<AEvent> CNMOD = new EventType<>(DSEventType.CN, "CNMOD");
	public static final EventType<AEvent> CNRON = new EventType<>(DSEventType.CN, "CNRON");
	public static final EventType<AEvent> CNRNN = new EventType<>(DSEventType.CN, "CNRNN");
}
