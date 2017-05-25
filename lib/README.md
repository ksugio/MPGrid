# Compile in Windows
Visual Studio Community, Python library and Zlib is required to create MPGrid.dll (MPGrid.pyd).
Setting of include path and library path is necessary to compile.
Set include path in [Property manager] - [Microsoft.cpp.Win32.user] - [VC++ Directory] - [Include directory].
Example is shown as follows.

`
C:\Python27\include
C:\Python27\Lib\site-packages\numpy\core\include
C:\lib\zlib128-dll\include
`
