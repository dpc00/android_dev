import java.io.IOException;

public interface IScanDir {
		public void findclose();
		public DE findfirst(String fs) throws IOException;
		public DE findnext() throws IOException;
	}

