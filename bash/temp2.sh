cd /sdcard/projects
git clone https://github.com/SDRplay/RSPTCPServer.git
cd RSPTCPServer
mkdir build
cd build
cmake ..
make
sudo make install