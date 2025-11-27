package org.ds.ui;

import javafx.beans.property.SimpleStringProperty;

public interface STRow {
	SimpleStringProperty bytesCopiedProperty();
	SimpleStringProperty bytesDeletedProperty();
	SimpleStringProperty dirsAddedProperty();
	SimpleStringProperty dirsCachedProperty();
	SimpleStringProperty dirsDeletedProperty();
	SimpleStringProperty dirsReadProperty();
	SimpleStringProperty errorCntProperty();
	SimpleStringProperty filesCopiedProperty();
	SimpleStringProperty filesDeletedProperty();
	SimpleStringProperty filesReadProperty();
	SimpleStringProperty rtProperty();
	SimpleStringProperty typeProperty();
	SimpleStringProperty volumeProperty();
}
