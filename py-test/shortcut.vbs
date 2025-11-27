   Dim crlf, ms
   crlf = Chr(13) & Chr(10)
   Set oWS = WScript.CreateObject("WScript.Shell")
   sLinkFile = "./Test1.LNK"
   Set oLink = oWS.CreateShortcut(sLinkFile)
   ms = "TargetPath: " & oLink.TargetPath & crlf
   ms = ms & "Arguments: " & oLink.Arguments & crlf
   ms = ms & "Description: " & oLink.Description & crlf
   ms = ms & "HotKey: " & oLink.HotKey & crlf
   ms = ms & "IconLocation: " & oLink.IconLocation & crlf
   ms = ms & "WindowStyle: " & oLink.WindowStyle & crlf
   ms = ms & "WorkingDirectory: " & oLink.WorkingDirectory & crlf
   WScript.Echo ms