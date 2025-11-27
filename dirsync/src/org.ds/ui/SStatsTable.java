package org.ds.ui;


import org.ds.app.DirSyncApp;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.control.TableView;

public class SStatsTable extends TableView<STRow> {

	public SStatsTable() { // 5 cols one row
		getColumns().add(SRow.tcs[0]);
		getColumns().add(SRow.tcs[1]);
		getColumns().add(SRow.tcscanned);
		getColumns().add(SRow.tcs[4]);
		getColumns().add(SRow.tcs[5]);

		ObservableList<STRow> rows = FXCollections.observableArrayList();
		rows.add(new SRow(DirSyncApp.it.dsl.d.first().ds));
		setItems(rows);
	}
}
