# CarolinaBaySedimentology

Visual database for sediment auger logs.

![GUI gif](https://github.com/mlundine/CarolinaBaySedimentology/blob/main/SedGUI.gif)

Installation:

Download repository.

Make a new Anaconda environment with python 3.7

conda create --name CarBaySedGUI python=3.7

Activate the environment.

conda activate CarBaySedGUI

install pyqt5 with:

pip install pyqt5 or conda install pyqt

SedGUI.py is the file to run in python.

cd to the CarolinaBaySedimentology folder.

cd wherever_you_placed_it/CarolinaBaySedimentology

Then run

python SedGUI.py 

Select a site, then click go to site and an image of the sediment will appear next to an image of the grain size histogram.

Above each sediment image is the name with the depth measurements in centimeters (top, bottom).

To go to a new site, first hit clear and then select the new site and then hit go to site.
