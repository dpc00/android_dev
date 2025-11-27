package org.ds.ui;

import java.text.NumberFormat;
import java.util.Locale;
import java.util.UnknownFormatConversionException;
import java.util.function.Function;

//import javafx.scene.control.skin.TableSkinUtils;
//import com.sun.javafx.scene.control.skin.Utils;
import javafx.application.Platform;
import javafx.scene.text.Text;
import org.ds.l4.DirSyncer;

import javafx.beans.binding.StringExpression;
import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;
import javafx.beans.value.ObservableValue;
import javafx.geometry.Pos;
import javafx.scene.control.TableCell;
import javafx.scene.control.TableColumn;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.util.Callback;

public class SRow implements STRow {
	public static TableColumn<STRow, String>[] tcs;
	public static TableColumn<STRow, String> tcaddedcopied;
	public static TableColumn<STRow, String> tcremoved;
	public static TableColumn<STRow, String> tcscanned;

	static NumberFormat nf = NumberFormat.getInstance(Locale.US);
//	static String fmtstr = DRow.fmtstr;
	DirSyncer ds;

	static int cc;
	static Callback<TableColumn<STRow, String>, TableCell<STRow, String>> cb1 = new Callback<TableColumn<STRow, String>, TableCell<STRow, String>>() {
		@Override
		public TableCell<STRow, String> call(TableColumn<STRow, String> col) {
			return cellType1(col);
		}
	};
	static Callback<TableColumn<STRow, String>, TableCell<STRow, String>> cb2 = new Callback<TableColumn<STRow, String>, TableCell<STRow, String>>() {
		@Override
		public TableCell<STRow, String> call(TableColumn<STRow, String> col) {
			return cellType2(col);
		}
	};
	SimpleStringProperty bcprop;
	SimpleStringProperty bdprop;
	SimpleStringProperty daprop;
	SimpleStringProperty dcprop;
	SimpleStringProperty ddprop;
	SimpleStringProperty drprop;
	SimpleStringProperty ecprop;
	SimpleStringProperty fcprop;
	SimpleStringProperty fdprop;
	SimpleStringProperty frprop;
	SimpleStringProperty rtprop;
	SimpleStringProperty typeprop;
	SimpleStringProperty volprop;
	StringExpression bcse;
	StringExpression bdse;
	StringExpression dase;
	StringExpression ddse;
	StringExpression drse;
	StringExpression fcse;
	StringExpression fdse;
	StringExpression frse;
	StringExpression ecse;
	StringExpression dcse;
	public SimpleStringProperty nulstr = new SimpleStringProperty("");

	static {
		tcs = new TableColumn[13];

		setStringColumn("Src/Tgt", STRow::typeProperty, cb1);
		setStringColumn("Root", STRow::rtProperty, cb1);
		setStringColumn("Volume", STRow::volumeProperty, cb1);
		setStringColumn("Dirs", STRow::dirsAddedProperty, cb2);
		setStringColumn("Files", STRow::filesCopiedProperty, cb2);
		setStringColumn("Bytes", STRow::bytesCopiedProperty, cb2);
		setStringColumn("Dirs", STRow::dirsDeletedProperty, cb2);
		setStringColumn("Files", STRow::filesDeletedProperty, cb2);
		setStringColumn("Bytes", STRow::bytesDeletedProperty, cb2);
		setStringColumn("Dirs", STRow::dirsReadProperty, cb2);
		setStringColumn("Files", STRow::filesReadProperty, cb2);
		setStringColumn("Cached Dirs", STRow::dirsCachedProperty, cb2);
		setStringColumn("Errors", STRow::errorCntProperty, cb2);

		tcaddedcopied = new TableColumn<>("Added/Copied");
		tcremoved = new TableColumn<>("Removed/Deleted");
		tcscanned = new TableColumn<>("Scanned");

		tcaddedcopied.getColumns().add(tcs[3]);
		tcaddedcopied.getColumns().add(tcs[4]);
		tcaddedcopied.getColumns().add(tcs[5]);

		tcremoved.getColumns().add(tcs[6]);
		tcremoved.getColumns().add(tcs[7]);
		tcremoved.getColumns().add(tcs[8]);

		tcscanned.getColumns().add(tcs[9]);
		tcscanned.getColumns().add(tcs[10]);
	}

	public SRow(DirSyncer ds) {
		this.ds = ds;
		this.bcprop = new SimpleStringProperty();
		this.bdprop = new SimpleStringProperty();
		this.daprop = new SimpleStringProperty();
		this.dcprop = new SimpleStringProperty();
		this.ddprop = new SimpleStringProperty();
		this.drprop = new SimpleStringProperty();
		this.ecprop = new SimpleStringProperty();
		this.fcprop = new SimpleStringProperty();
		this.fdprop = new SimpleStringProperty();
		this.frprop = new SimpleStringProperty();
		this.typeprop = new SimpleStringProperty("Source");
		this.rtprop = new SimpleStringProperty(this.ds.s.st.Fp().s);
		this.volprop = new SimpleStringProperty(this.ds.s.st.Vl().s);

		this.bcse = DRow.bind_format2((ObservableValue<Number>)this.ds.bytescopied.p);
		this.bdse = DRow.bind_format2((ObservableValue<Number>)this.ds.bytesdeleted.p);
		this.dase = DRow.bind_format1((ObservableValue<Number>)this.ds.dirsadded.p);
		this.dcse = DRow.bind_format1((ObservableValue<Number>)this.ds.s.cc.dirscached.p);
		this.ddse = DRow.bind_format1((ObservableValue<Number>)this.ds.dirsdeleted.p);
		this.drse = DRow.bind_format1((ObservableValue<Number>)this.ds.s.cc.dirsread.p);
		this.ecse = DRow.bind_format1((ObservableValue<Number>)this.ds.errorcnt.p);
		this.fcse = DRow.bind_format1((ObservableValue<Number>)this.ds.filescopied.p);
		this.fdse = DRow.bind_format1((ObservableValue<Number>)this.ds.filesdeleted.p);
		this.frse = DRow.bind_format1((ObservableValue<Number>)this.ds.s.cc.filesread.p);

		this.bcprop.bind(this.bcse);
		this.bdprop.bind(this.bdse);
		this.daprop.bind(this.dase);
		this.dcprop.bind(this.dcse);
		this.ddprop.bind(this.ddse);
		this.drprop.bind(this.drse);
		this.ecprop.bind(this.ecse);
		this.fcprop.bind(this.fcse);
		this.fdprop.bind(this.fdse);
		this.frprop.bind(this.frse);
	}

	public final static Font cf = Font.font("Monospaced", 12.0);
	public final static Text theText = new Text();

	static {
		theText.setFont(cf);
	}

	public static TableCell<STRow, String> cellType1(TableColumn<STRow, String> col) {
		final TableCell<STRow, String> tc = new TableCell<STRow, String>() {
			@Override
			protected void updateItem(String item, boolean empty) {
				super.updateItem(item, empty);
				setText(item);
				if(!empty) {
					theText.setText(getText());
					double dw = theText.getBoundsInLocal().getWidth() + 16.0;
					double cw = col.getWidth();
					if (dw > cw) {
						Platform.runLater(() -> {
							col.setPrefWidth(dw);
						});
					}
				}
//				TableSkinUtils.resizeColumnToFitContent(tc.getTableView().getSkin(),tc.getTableColumn(),30);
//				TableSkinUtils.resizeColumnToFitContent(tc.getTableView(),tc.getTableColumn(),tc.getTableView().getSkin(), 30);
			}
		};
		tc.setAlignment(Pos.TOP_CENTER);
		tc.setFont(cf);
		tc.setTextFill(Color.BLUE);
		return tc;
	}

	public static TableCell<STRow, String> cellType2(TableColumn<STRow, String> col) {
		final TableCell<STRow, String> tc = new TableCell<STRow, String>() {
			@Override
			protected void updateItem(String item, boolean empty) {
				super.updateItem(item, empty);
				setText(item);
				// check here if col too small
//				Utils.computeTextWidth(tc.getFont(),item, 0);
				if(!empty) {
					theText.setText(getText());
					double dw = theText.getBoundsInLocal().getWidth() + 16.0;
					double cw = col.getWidth();
					if (dw > cw) {
						Platform.runLater(() -> {
								col.setPrefWidth(dw);
						});
					}
				}
//				TableSkinUtils.resizeColumnToFitContent(tc.getTableView().getSkin(),tc.getTableColumn(),30);
//				TableSkinUtils.resizeColumnToFitContent(tc.getTableView(),tc.getTableColumn(),tc.getTableView().getSkin(), 30);
			}
		};
		tc.setAlignment(Pos.TOP_RIGHT);
		tc.setFont(cf);
		tc.setTextFill(Color.ORANGERED);
		return tc;
	}

	public static void setStringColumn(String title, Function<STRow, StringProperty> fn,
		Callback<TableColumn<STRow, String>, TableCell<STRow, String>> cb) {
		int i = cc++;
		tcs[i] = new TableColumn<>();
		tcs[i].setText(title);
		tcs[i].setCellValueFactory(row -> {
			try {
				return fn.apply(row.getValue());
			} catch (UnknownFormatConversionException ex) {
				return new SimpleStringProperty("err");
			}
		});
		tcs[i].setCellFactory(cb);
	}

	public SimpleStringProperty typeProperty() {
		return this.typeprop;
	}

	public SimpleStringProperty rtProperty() {
		return this.rtprop;
	}

	public SimpleStringProperty volumeProperty() {
		return this.volprop;
	}

	public SimpleStringProperty bytesCopiedProperty() {
		return this.nulstr; // bcprop;
	}

	public SimpleStringProperty bytesDeletedProperty() {
		return this.nulstr; // bdprop;
	}

	public SimpleStringProperty dirsAddedProperty() {
		return this.nulstr; // daprop;
	}

	public SimpleStringProperty dirsDeletedProperty() {
		return this.nulstr; // ddprop;
	}

	public SimpleStringProperty dirsReadProperty() {
		return this.drprop;
	}

	public SimpleStringProperty filesCopiedProperty() {
		return this.nulstr; // fcprop;
	}

	public SimpleStringProperty filesDeletedProperty() {
		return this.nulstr; // fdprop;
	}

	public SimpleStringProperty filesReadProperty() {
		return this.frprop;
	}

	public SimpleStringProperty dirsCachedProperty() {
		return this.dcprop;
	}

	public SimpleStringProperty errorCntProperty() {
		return this.nulstr; // ecprop;
	}

}
