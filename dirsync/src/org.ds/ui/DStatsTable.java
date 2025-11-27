package org.ds.ui;


import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

// import javafx.scene.control.skin.TableSkinUtils;
//import com.sun.javafx.scene.control.skin.TableSkinUtils;


import javafx.event.Event;
import javafx.scene.control.TableCell;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.skin.*;
import javafx.scene.input.MouseButton;
import javafx.scene.input.MouseEvent;
import javafx.scene.input.PickResult;

public class DStatsTable extends TableView<STRow> {
	private static Method columnToFitMethod;
	 static {
//	 	try {
//			 columnToFitMethod = TableSkinUtils.class.getDeclaredMethod("resizeColumnToFitContent", TableColumn.class, int.class);
//			 columnToFitMethod.setAccessible(true);
//	 	} catch (NoSuchMethodException e) {
//	 		e.printStackTrace();
//	 	}
	 }

	public static void autoFitCol(TableView<STRow> tableView, TableCell<STRow, String> tc) {
		TableColumn<STRow, String> col = tc.getTableColumn();
		col.setMinWidth(col.getWidth() + .1);
	}

	public DStatsTable() {
		getColumns().add(DRow.tcs[0]);
		getColumns().add(DRow.tcs[1]);
		getColumns().add(DRow.tcs[2]);

		getColumns().add(DRow.tcscanned);
		getColumns().add(DRow.tcaddedcopied);
		getColumns().add(DRow.tcremoved);

		getColumns().add(DRow.tcs[11]);
		getColumns().add(DRow.tcs[12]);

	}
}
