# Compile in Windows
Visual Studio Community and Python library are required to create MPCLGrid.dll (MPCLGrid.pyd).
Open MPGLGrid.sln and set include path and library path according to [Property Manager] - [Microsoft.cpp.Win32.user] - [VC++ Directory] - [Include Directory] and [Library Directory].
Example of include path is shown.

    C:\Python27\include
    C:\Python27\Lib\site-packages\numpy\core\include

Example of library path is shown.

    C:\Python27\libs
    C:\Python27\Lib\site-packages\numpy\core\lib

Build in Release mode and MPGLGrid.pyd is copied to python directory.

# Compile in Linux
Edit Makefile and execute make.

    vi Makefile
    make install

MPGLGrid.so is created and copied to python directory.

# References
+ METHODS
  + platform_info(id) : platform information
  + platform_num() : number of platform

## Class new(...)
+ new(grid, id)
  + grid : grid data
  + id : platform id
+ CLASS METHODS
  + solve(grid, dt, nloop) : solve
