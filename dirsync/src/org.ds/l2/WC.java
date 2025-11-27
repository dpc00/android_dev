package org.ds.l2;

import java.nio.charset.Charset;
// import java.nio.charset.StandardCharsets;

public class WC {
	// file attributes
	public static final int FA_READONLY = 1;
	public static final int FA_HIDDEN = 2;
	public static final int FA_SYSTEM = 4;
	public static final int FA_DIRECTORY = 16;
	public static final int FA_ARCHIVE = 32;
	public static final int FA_DEVICE = 64;
	public static final int FA_NORMAL = 128;
	public static final int FA_TEMPORARY = 256;
	public static final int FA_SPARSE_FILE = 512;
	public static final int FA_REPARSE_POINT = 1024;
	public static final int FA_COMPRESSED = 2048;
	public static final int FA_OFFLINE = 4096;
	public static final int FA_NOT_CONTENT_INDEXED = 8192;
	public static final int FA_ENCRYPTED = 16384;
	public static final int FA_INTEGRITY_STREAM = 32768;
	public static final int FA_VIRTUAL = 65536;
	public static final int FA_NO_SCRUB_DATA = 131072;

	public static final int OPEN_EXISTING = 3;

	public static final int MAX_PATH1 = 260;
	public static final int MAX_PATH2 = 32767;

	// Number of seconds, etc. between 1601-01-01 and 1970-01-01
	public static final long SECONDS_BETWEEN_EPOCHS = 11644473600L;
	public static final long MILLISECONDS_BETWEEN_EPOCHS = 11644473600000L;
	public static final long MICROSECONDS_BETWEEN_EPOCHS = 11644473600000000L;
	public static final long HUNDREDNANOSECONDS_BETWEEN_EPOCHS = 116444736000000000L;

	public static final int INVALID_HANDLE_VALUE = -1;
	public static final int INVALID_FILE_ATTRIBUTES = -1;

	// windows error codes
	public static final int WE_INVALID_FUNCTION = 1;
	public static final int WE_FILE_NOT_FOUND = 2;
	public static final int WE_PATH_NOT_FOUND = 3;
	public static final int WE_ACCESS_DENIED = 5;
	public static final int WE_INVALID_HANDLE = 6;
	public static final int WE_NO_MORE_FILES = 18;
	public static final int WE_SHARING_VIOLATION = 32;
	public static final int WE_LOCK_VIOLATION = 33;
	public static final int WE_FILE_EXISTS = 80;
	public static final int WE_INVALID_PARAMETER = 87;
	public static final int WE_BAD_PATH_NAME = 161;
	public static final int WE_ALREADY_EXISTS = 183;
	public static final int WE_OPERATION_ABORTED = 995;
	public static final int WE_NOTIFY_ENUM_DIR = 1022;
	public static final int WE_UNABLE_TO_REMOVE_REPLACED = 1175;
	public static final int WE_UNABLE_TO_MOVE_REPLACEMENT = 1176;
	public static final int WE_UNABLE_TO_MOVE_REPLACEMENT_2 = 1177;

	public static final long IO_REPARSE_TAG_SYMLINK = 0xA000000CL;

	public static final long FAT32_GRANULARITY = 20000000L;

	// Change notification filters
	public static final int NF_FILE_NAME = 1;
	public static final int NF_DIR_NAME = 2;
	public static final int NF_ATTRIBUTES = 4;
	public static final int NF_SIZE = 8;
	public static final int NF_LAST_WRITE = 16;
	public static final int NF_CREATION = 64;
	public static final int NF_SECURITY = 256;
	// Change notification 'event' org.ds.types
	public static final int CNE_ADDED = 1;
	public static final int CNE_REMOVED = 2;
	public static final int CNE_MODIFIED = 3;
	public static final int CNE_RENAMED_OLD_NAME = 4;
	public static final int CNE_RENAMED_NEW_NAME = 5;
	public static final int INFINITE = -1;
	public static final int WAIT_FAILED = -1;
	public static final int FILE_LIST_DIRECTORY = 1;
	public static final int FILE_FLAG_BACKUP_SEMANTICS = 0x2000000;
	public static final int FILE_SHARE_READ = 1;
	public static final int FILE_SHARE_WRITE = 2;
	public static final int FILE_SHARE_DELETE = 4;
	public static final Charset CHARSET = Charset.defaultCharset();
	public static final int FORMAT_MESSAGE_FROM_SYSTEM = 0x00001000;
	public static final int RF_WRITE_THROUGH = 0X00000001;
	public static final int RF_IGNORE_MERGE_ERRORS = 0x00000002;
	public static final int RF_IGNORE_ACL_ERRORS = 0x00000004;
	public static final int SND_SYNC = 0x0000; /* play synchronously (default) */
	public static final int SND_ASYNC = 0x0001; /* play asynchronously */
	public static final int SND_NODEFAULT = 0x0002; /*
																	 * silence (!default) if
																	 * sound not found
																	 */
	public static final int SND_MEMORY = 0x0004; /*
																 * pszSound points to a memory
																 * file
																 */
	public static final int SND_LOOP = 0x0008; /*
																 * loop the sound until next
																 * sndPlaySound
																 */
	public static final int SND_NOSTOP = 0x0010; /*
																 * don't stop any currently
																 * playing sound
																 */
	public static final int SND_NOWAIT = 0x00002000; /*
																		 * don't wait if the
																		 * driver is busy
																		 */
	public static final int SND_ALIAS = 0x00010000; /*
																	 * name is a registry alias
																	 */
	public static final int SND_ALIAS_ID = 0x00110000; /* alias is a pre d ID */
	public static final int SND_FILENAME = 0x00020000; /* name is file name */
	public static final int SND_RESOURCE = 0x00040004; /*
																		 * name is resource name
																		 * or atom
																		 */
	public static final int SND_PURGE = 0x0040; /*
																 * purge non-static events for
																 * task
																 */
	public static final int SND_APPLICATION = 0x0080; /*
																		 * look for application
																		 * specific association
																		 */
	public static final int NF_LAST_ACCESS = 32;
	public static final int NF_ALL = WC.NF_FILE_NAME | WC.NF_DIR_NAME | WC.NF_ATTRIBUTES | WC.NF_SIZE | WC.NF_LAST_WRITE
			| WC.NF_LAST_ACCESS | WC.NF_CREATION | WC.NF_LAST_ACCESS | WC.NF_SECURITY;
}
