package org.ds.git;

import java.io.File;
import java.io.StringWriter;
import java.util.ArrayList;
import java.util.Optional;
import java.util.Properties;
import java.util.Set;
import java.util.StringJoiner;
import java.util.TreeSet;
import java.util.function.BiConsumer;
import java.util.function.Supplier;
import java.util.stream.Collectors;

import org.ds.app.DirSyncApp;
import org.ds.l3.DSubs;
import org.ds.l4.DirScanner;
import org.ds.types.DItem;
import org.ds.types.FP;
import org.ds.types.RD;
import org.ds.types.ST;
import org.ds.ui.TextWrap;
import org.eclipse.jgit.api.AddCommand;
import org.eclipse.jgit.api.CloneCommand;
import org.eclipse.jgit.api.CommitCommand;
import org.eclipse.jgit.api.GarbageCollectCommand;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.PushCommand;
import org.eclipse.jgit.api.Status;
import org.eclipse.jgit.api.StatusCommand;
import org.eclipse.jgit.dircache.DirCache;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.lib.TextProgressMonitor;
import org.eclipse.jgit.revwalk.RevCommit;
import org.eclipse.jgit.storage.file.FileRepositoryBuilder;
import org.eclipse.jgit.transport.CredentialsProvider;
import org.eclipse.jgit.transport.NetRCCredentialsProvider;
import org.eclipse.jgit.transport.PushResult;
import org.eclipse.jgit.transport.RemoteRefUpdate;
import org.eclipse.jgit.util.FS;

public class GitFunctions {
	private static CredentialsProvider cp = new NetRCCredentialsProvider();
	private Git g;
	private Repository r;

	private GitFunctions(FP fp) {
		try {
			FileRepositoryBuilder frb = new FileRepositoryBuilder();
			frb.readEnvironment();
			frb.setGitDir(new File(fp.s));
			frb.setWorkTree(new File(DSubs.getParent(fp.s)));
			frb.setMustExist(true);
			this.r = frb.build();
			this.g = Git.wrap(this.r);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public static void doGCs(ST st) {
		FS.DETECTED.setUserHome(new File(st.Fp().s));
		ArrayList<FP> fpl = findRepos(st);
		if (fpl.isEmpty())
			return;
		fpl.sort(GitFunctions::compareGDs);
		for (FP fp : fpl) {
			TextWrap.it.taprintln("attempting to garbage collect " + fp);
			Optional<GitFunctions> ogf = Optional.empty();
			try {
				ogf = GitFunctions.newGF(fp);
				if (ogf.isPresent()) {
					GitFunctions gf = ogf.get();
					gf.git_gc();
				} else {
					TextWrap.it.taprintln("something went wrong with Git|Repo init");
				}
			} finally {
				ogf.ifPresent(GitFunctions::repo_close);
			}
		}
	}

	public static void doUpdates() {
		doUpdates(DirSyncApp.it.dsl.s.st);
	}

	public static void git_clone(ST st, String url, File tgt) {
		FS.DETECTED.setUserHome(new File(st.Fp().s));
			Optional<GitFunctions> ogf = Optional.empty();
			try {
				CloneCommand cc = new CloneCommand();
				cc.setURI(url);
				cc.setDirectory(tgt);
				cc.call();
			}
			catch(Exception e) {
				e.printStackTrace();
			}
			finally {
				ogf.ifPresent(GitFunctions::repo_close);
			}
	}

	public static void doUpdates(ST st) {
		FS.DETECTED.setUserHome(new File(st.Fp().s));
		ArrayList<FP> fpl = findRepos(st);
		if (fpl.isEmpty())
			return;
		fpl.sort(GitFunctions::compareGDs);
		for (FP fp : fpl) {
			TextWrap.it.taprintln("attempting to update " + fp);
			Optional<GitFunctions> ogf = Optional.empty();
			try {
				ogf = GitFunctions.newGF(fp);
				if (ogf.isPresent()) {
					GitFunctions gf = ogf.get();
					Optional<Set<String>> oss = gf.git_status();
					if (oss.isPresent()) {
						gf.git_add(oss.get());
						oss = gf.git_status();
					}
					oss.ifPresent(strings -> gf.git_commit("abcde"));
					gf.git_push();
				} else {
					TextWrap.it.taprintln("something went wrong with Git/Repo init");
				}
			} finally {
				ogf.ifPresent(GitFunctions::repo_close);
			}
		}
	}

	public static Optional<GitFunctions> newGF(FP fp) {
		GitFunctions gf = new GitFunctions(fp);
		if (gf.g == null || gf.r == null) {
			gf.repo_close();
			return Optional.empty();
		}
		return Optional.of(gf);
	}

	public static int compareGDs(FP o1, FP o2) {
		int pic1 = o1.s.split("\\\\").length;
		int pic2 = o2.s.split("\\\\").length;
		int d1 = pic1 - pic2;
		if (d1 == 0) {
			return o1.s.compareTo(o2.s);
		}
		return -d1;
	}

	public static ArrayList<FP> findRepos() {
		return findRepos(DirSyncApp.it.dsl.s.st);
	}

	public static ArrayList<FP> findRepos(ST st) {
		DItem sd = st.SDir(new RD("Projects")); // DSubs.resolve(dssi.st.Fp().s, "Projects")
		DirScanner ds = new DirScanner(sd);
		ArrayList<FP> fpl = ds.find(fp -> fp.s.endsWith("\\.git"));
		return fpl;
	}

	private DirCache git_add(Set<String> ss) {
		try {
			TextWrap.it.taprintln("calling git_add");
			AddCommand ac = this.g.add();
			for (String s : ss) {
				ac.addFilepattern(s);
			}
			if (ss.size() == 0) {
				ac.addFilepattern(".");
			}
			return ac.call();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}

	private void repo_close() {
		if (this.r != null)
			this.r.close();
	}

	private RevCommit git_commit(String msg) {
		try {
			TextWrap.it.taprintln("calling git_commit");
			CommitCommand cc = this.g.commit();
			cc.setAll(true);
			cc.setMessage(msg);
			RevCommit rc = cc.call();
			TextWrap.it.taprintln("\t" + rc.toString());
			return rc;
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}

	private String formatResponse(StringWriter sw) {
		ArrayList<String> sl = new ArrayList<>();
		String s = sw.toString().trim();
		String[] sa = s.split("\n");
		for (String s2 : sa) {
			String[] sa2 = s2.split("\r");
			sl.add(sa2[sa2.length - 1]);
		}
		return "\t" + sl.stream().collect(Collectors.joining("\n\t"));
	}

	private void git_gc() {
		try {
			TextWrap.it.taprintln("calling git_gc");
			GarbageCollectCommand gc = this.g.gc();
			StringWriter sw = new StringWriter();
			gc.setProgressMonitor(new TextProgressMonitor(sw));
			gc.setAggressive(true);
			gc.setPrunePreserved(true);
			gc.setPreserveOldPacks(false);
			Properties p = gc.call();
			TextWrap.it.taprintln(formatResponse(sw));
			String ps = p.entrySet().stream().map((me) -> me.getKey() + ": " + me.getValue()).collect(Collectors.joining("\n\t\t"));
			TextWrap.it.taprintln("\t\t" + ps);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private void printPushResults(Iterable<PushResult> it) {
		for (PushResult pr : it) {
			StringJoiner joiner = new StringJoiner("\n\t");
			for (RemoteRefUpdate rru : pr.getRemoteUpdates()) {
				RemoteRefUpdate.Status status = rru.getStatus();
				joiner.add(status.name());
			}
			TextWrap.it.taprintln("\t" + joiner.toString());
		}
	}

	private void printStatus(Status st) {
		BiConsumer<String, Supplier<Set<String>>> bf1 = (name, ss) -> {
			for (String s : ss.get()) {
				TextWrap.it.taprintln("\t" + name + ": " + s);
			}
		};
		bf1.accept("added", st::getAdded);
		bf1.accept("changed", st::getChanged);
		bf1.accept("conflicting", st::getConflicting);
		// bf1.accept("ignorednotinindex", st::getIgnoredNotInIndex);
		bf1.accept("missing", st::getMissing);
		bf1.accept("modified", st::getModified);
		bf1.accept("removed", st::getRemoved);
		// bf1.accept("untracked", st::getUntracked);
		// bf1.accept("untrackedfolders", st::getUntrackedFolders);
	}

	private void git_push() {
		try {
			TextWrap.it.taprintln("calling git_push");
			PushCommand pc = this.g.push();
			StringWriter sw = new StringWriter();
			pc.setProgressMonitor(new TextProgressMonitor(sw));
			pc.setPushAll();
			pc.setTimeout(2000);
			pc.setCredentialsProvider(cp);
			pc.setForce(true);
			Iterable<PushResult> it = pc.call();
			TextWrap.it.taprintln(formatResponse(sw));
			printPushResults(it);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private Optional<Set<String>> git_status() {
		try {
			TextWrap.it.taprintln("calling git_status");
			StatusCommand sc = this.g.status();
			StringWriter sw = new StringWriter();
			sc.setProgressMonitor(new TextProgressMonitor(sw));
			Status s = sc.call();
			TextWrap.it.taprintln(formatResponse(sw));
			if (!s.isClean()) {
				printStatus(s);
				Set<String> ss = new TreeSet<>();
				ss.addAll(s.getAdded());
				ss.addAll(s.getChanged());
				ss.addAll(s.getMissing());
				ss.addAll(s.getModified());
				ss.addAll(s.getRemoved());
				return Optional.of(ss);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return Optional.empty();
	}

}
