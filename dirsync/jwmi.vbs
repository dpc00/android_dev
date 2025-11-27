Dim oWMI
Set oWMI = GetObject("winmgmts:")
Dim classComponent
Set classComponent = oWMI.ExecQuery("wmic VOLUME get capacity,driveletter,filesystem,freespace,label,serialnumber")
Dim obj
Dim strData
For Each obj in classComponent
  Set strData = strData & obj.capacity & VBCrLf
  Set strData = strData & obj.driveletter & VBCrLf
  Set strData = strData & obj.filesystem & VBCrLf
  Set strData = strData & obj.freespace & VBCrLf
  Set strData = strData & obj.label & VBCrLf
  Set strData = strData & obj.serialnumber & VBCrLf
Next
wscript.echo strData
