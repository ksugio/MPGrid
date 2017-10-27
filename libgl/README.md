# Compile in Windows
Visual Studio Community and Python library are required to create MPGLGrid.dll (MPGLGrid.pyd).
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
+ CLASS
 + colormap()
   + CLASS METHODS
     + color() : set default color
     + draw() : draw colormap
     + grad_color(value) : get grad color
     + grayscale() : set default grayscale
     + set_grad_color(id, red, green, blue) : set grad color
     + set_label(id, label) : set label
     + set_step_color(id, red, green, blue) : set step color
     + step_color(id) : get step color
   + CLASS DATA
     + font_color = (red, green, blue) : font color
     + font_type = {0:10pt | 1:12pt | 2:18pt} : font type
     + mode = {0:step | 1:gradation} : colormap mode
     + ngrad = num : number of gradiation color
     + nscale = num : number of scale
     + nstep = num : number of step color
     + range = (min, max) : colormap range
     + size = (width, height) : colormap size
     + title = txt : colormap title
