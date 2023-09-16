# iHVI tool
Heat Vulnerability Index open source desktop toolkit

## Summary
The iHVI toolkit constructs heat sensitivity, heat adaptive capability indicators, and composite heat vulnerability index, which enables modelling of the relationships between heat, environmental and socio-economic factors. This desktop-based application is a first nationwide, dynamic and interactive heat vulnerability assessment toolkit with enhanced workflow, automated analysis and modelling tools, so the indicators and indices can be updated and constructed by the users to serve more applications.  

## System architecture 
The iHVI system interface operates based on the [iGEE tool](http://www.gisonmeta.com) and [ABS](https://www.abs.gov.au/census) census data. Users can access the iGEE and ABS websites by clicking the buttons on the first row. The data input buttons are on the second row, including LST, NDVI, NDBI, Population Density, Population over 65 years old, Population less than 4 years old, Population Needs Care, Education Level, and Income Level. By default, the “|” below these buttons is “X”, indicating that the input data is empty. When users click on the second row of input buttons, they will be asked to choose files from their local file system, and the “X” will change to a “|.”  The heat exposure index, heat sensitivity index, and adaptive capability index can be calculated when the correspondingly coloured input data has been filled in. If all the data is uploaded, users can click the blue buttons to calculate the heat vulnerability index and heat vulnerability score. The output destination is the same directory as the one where the iHVI desktop application is located. Users can define a different output folder by clicking on the “Select folder” button in the bottom right corner. If any errors occur during the calculation, the app will prompt the user with a warning and the user can make changes accordingly.  

Architecture: 

## iHVI application

Please use python 3.8+ or higher.

Please adjust your PC/laptop's display scale to 100% to avoid squeezed content.

Environment configuration:

```console
pip install --upgrade PySimpleGUIQt  
pip install --upgrade pandas
```

Or if you are using conda environment, run:
```console
conda install -c conda-forge pysimpleguiqt
conda install -c anaconda pandas
```

Download the code from this repository and run:
```console
python mainApp.py
```
----
Or you can directly run "output/mainApp/mainApp.exe" on windows operating system.

##Technical documentation

[iHVI User Manual](Documentation.md)


**iHVI publication**

Access to iHVI: AN OPEN-SOURCE TOOLKIT FOR CONSTRUCTING INTEGRATED HEAT VULNERABILITY INDEX IN AUSTRALIA : https://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XLVIII-4-W5-2022/175/2022/isprs-archives-XLVIII-4-W5-2022-175-2022.pdf 
