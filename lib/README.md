# Compile in Windows
Visual Studio Community, Python library and Zlib is required to create MPGrid.dll (MPGrid.pyd).
Open MPGrid.sln and set include path and library path according to [Property Manager] - [Microsoft.cpp.Win32.user] - [VC++ Directory] - [Include Directory] and [Library Directory].
Example of include path is shown.

    C:\Python27\include
    C:\Python27\Lib\site-packages\numpy\core\include
    C:\lib\zlib128-dll\include

Example of library path is shown.

    C:\Python27\libs
    C:\Python27\Lib\site-packages\numpy\core\lib
    C:\lib\zlib128-dll\lib

Build in Release mode and MPGrid.pyd is copied to python directory.

# Compile in Linux
Edit Makefile and execute make.

    vi Makefile
    make install

MPGrid.so is created and copied to python directory.
