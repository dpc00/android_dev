setlocal
set sr=%FLASH0%
set dr=%FLASH1%
set rd=\
del temp*.bat
echo call test-sub1 %sr% %dr% %rd%>temp.bat
temp.bat