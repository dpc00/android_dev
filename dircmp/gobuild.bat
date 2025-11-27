set GOPATH=%FLASH0%\Go;%FLASH0%\Projects\DirCmp
go fmt org/dc
go build -o bin\dircmp.exe org/dc