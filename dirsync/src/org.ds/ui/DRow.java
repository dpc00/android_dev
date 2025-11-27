package org.ds.ui;

import javafx.beans.binding.Bindings;
import javafx.beans.binding.StringExpression;
import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;
import javafx.beans.value.ObservableValue;
import javafx.scene.control.TableCell;
import javafx.scene.control.TableColumn;
import javafx.util.Callback;
import org.ds.l4.DirSyncer;

import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.Locale;
import java.util.UnknownFormatConversionException;
import java.util.function.Function;

import static org.ds.ui.SRow.cb1;
import static org.ds.ui.SRow.cb2;

@SuppressWarnings("unchecked")
public class DRow implements STRow {
	public static TableColumn<STRow, String>[] tcs;
	public static TableColumn<STRow, String> tcaddedcopied;
	public static TableColumn<STRow, String> tcremoved;
	public static TableColumn<STRow, String> tcscanned;

	static NumberFormat nf = DecimalFormat.getInstance(Locale.US);
	static String fmtstr = "%,2d";
	DirSyncer ds;

	static int cc;

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

	static {

		tcs = new TableColumn[13];
// sort not
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

	public DRow(DirSyncer ds) {
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
		this.typeprop = new SimpleStringProperty("Target");
		this.rtprop = new SimpleStringProperty(this.ds.d.st.Fp().s);
		this.volprop = new SimpleStringProperty(this.ds.d.st.Vl().s);

		this.bcse = bind_format1((ObservableValue<Number>) this.ds.bytescopied.p);
		this.bdse = bind_format1((ObservableValue<Number>) this.ds.bytesdeleted.p);
		this.dase = bind_format1((ObservableValue<Number>) this.ds.dirsadded.p);
		this.dcse = bind_format1((ObservableValue<Number>) this.ds.d.cc.dirscached.p);
		this.ddse = bind_format1((ObservableValue<Number>) this.ds.dirsdeleted.p);
		this.drse = bind_format1((ObservableValue<Number>) this.ds.d.cc.dirsread.p);
		this.ecse = bind_format1((ObservableValue<Number>) this.ds.errorcnt.p);
		this.fcse = bind_format1((ObservableValue<Number>) this.ds.filescopied.p);
		this.fdse = bind_format1((ObservableValue<Number>) this.ds.filesdeleted.p);
		this.frse = bind_format1((ObservableValue<Number>) this.ds.d.cc.filesread.p);

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

	public static StringExpression bind_format1(ObservableValue<Number> p) {
		return Bindings.format("%,d", p);
	}

	public static StringExpression bind_format2(ObservableValue<Number> p) {
		return Bindings.format("%,d", p);
	}

	public static void setStringColumn(String title, Function<STRow, StringProperty> fn,
		Callback<TableColumn<STRow, String>, TableCell<STRow, String>> cb) {
		int i = cc++;
		tcs[i] = new TableColumn<>();
		tcs[i].setText(title);
		tcs[i].setCellValueFactory(
			new Callback<TableColumn.CellDataFeatures<STRow, String>, ObservableValue<String>>() {
				@Override
				public ObservableValue<String> call(TableColumn.CellDataFeatures<STRow, String> cdf) {
					try {
						return fn.apply(cdf.getValue()); // value is the STRow, fn is the property getter function
					} catch (UnknownFormatConversionException ex) {
						return new SimpleStringProperty("fmterr");
					}
				}
			}
		);
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
		return this.bcprop;
	}

	public SimpleStringProperty bytesDeletedProperty() {
		return this.bdprop;
	}

	public SimpleStringProperty dirsAddedProperty() {
		return this.daprop;
	}

	public SimpleStringProperty dirsDeletedProperty() {
		return this.ddprop;
	}

	public SimpleStringProperty dirsReadProperty() {
		return this.drprop;
	}

	public SimpleStringProperty filesCopiedProperty() {
		return this.fcprop;
	}

	public SimpleStringProperty filesDeletedProperty() {
		return this.fdprop;
	}

	public SimpleStringProperty filesReadProperty() {
		return this.frprop;
	}

	public SimpleStringProperty errorCntProperty() {
		return this.ecprop;
	}

	public SimpleStringProperty dirsCachedProperty() {
		return this.dcprop;
	}

}
