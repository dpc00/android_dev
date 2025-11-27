path %~d0\Programs\Node;%path%
set NODE_PATH=%~d0\Programs\Node\node_modules;%~d0\Projects\tools\lib
%~d0
cd \projects\tools
jake.cmd cpl:bat
