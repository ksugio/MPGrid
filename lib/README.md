# Compile in Windows
Visual Studio Community, Python library and Zlib is required to create MPGrid.dll (MPGrid.pyd).
Open MPGrid.sln in lib directory.
Setting of include path and library path is necessary to compile.
Set include path in [Property Manager] - [Microsoft.cpp.Win32.user] - [VC++ Directory] - [Include Directory].
Example of include path

    C:\Python27\include
    C:\Python27\Lib\site-packages\numpy\core\include
    C:\lib\zlib128-dll\include

Build in Release mode and MPGrid.pyd is copied to python directory.

# Compile in Linux
Edit Makefile and execute make.

    vi Makefile
    make install

MPGrid.so is created and copied to python directory.
