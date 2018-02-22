# XElanQ
Python script for creating a CSV file from an output (*.rep* files) generated by the software of Perkin Elmer Elan DRC II Inductively Coupled  Plasma Mass Spectrometer (ICP-MS)

## How to use
This is a Python3 script, so you should have Python3 installed before attempting to use this.
Simply run in your prefered terminal or command line:

    python3 xelanq

and you should have an output.csv files with the result in the current directory. Tested on Linux, Windows 10 and macOS. The script needs a proper *tq.rep* file in the current directory, as input.

## Changelog

### Version 0.1a – Tarsus IV's moon (22.02.2018)
*Functional, but limited*

- Changed the separator from comma to semicolon, to mitigate the problems that might appear during Excel import, due to regional settings
- Rounded the concentration values when exported
- Optimized the array size, based on exact values: detected number of samples and actual number of elements
- Added support for choosing the file from current directory
- Saving keeps the name of the original file, but changes extension to *.csv*
- Some hard-coded values related to search within the file were removed
- Code was restructured

### Version 0.1 – Tarsus IV (initial release, 21.02.2018)
*Functional, but limited*

This is more like a proof-of-concept. The script reads the *.rep* file and outputs a (proper) CSV file, with all the samples ordered in columns, with element concentration on each line. Only works for (my) TotalQuant report files, but support for quantitative reports is planned in future versions.

## TODO

- Support for some data processing
- General code optimization (?)
- Support for quantitative analysis reports
- Better error handling
