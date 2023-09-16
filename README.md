# iHVI tool - Heat Vulnerability Index open source desktop toolkit

Access to publication - iHVI: AN OPEN-SOURCE TOOLKIT FOR CONSTRUCTING INTEGRATED HEAT VULNERABILITY INDEX IN AUSTRALIA : https://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XLVIII-4-W5-2022/175/2022/isprs-archives-XLVIII-4-W5-2022-175-2022.pdf 

## Summary
The iHVI toolkit constructs heat sensitivity, heat adaptive capability indicators, and composite heat vulnerability index, which enables modelling of the relationships between heat, environmental and socio-economic factors. This desktop-based application is a first nationwide, dynamic and interactive heat vulnerability assessment toolkit with enhanced workflow, automated analysis and modelling tools, so the indicators and indices can be updated and constructed by the users to serve more applications.  

## Conceptual framework  

The diagram shows the conceptual heat vulnerability assessment framework. It is a four-stage assessment framework to derive heat vulnerability index by calculating heat exposure index, heat sensitivity index and adaptive capability index for intervention strategies. 
HVI is calculated as : Heat Vulnerability Index (HVI) = Heat Exposure index + Heat Sensitivity index - Adaptive Capacity Index 

<img width="100%" alt="image" src="https://github.com/IGEE-IHVI/iHVI-app/blob/main/HVI%20conceptual%20framework.png">

## iHVI application

The iHVI desktop toolkit  was developed in the Python 3 environment. The primary packages consist of PySimpleGUIQt, Pandas, Numpy, and other Python builtin packages. PySimpleGUIQt is an integrated package for frontend user interface development. The Pandas and Numpy are mainly used for the heat vulnerability index and heat vulnerability score calculation functions’ development. The software compilation is based on the auto-pyto-exe converter, which is a Python-based converter that can compile Python files (.py) to executable files (.exe). The executable file will not require manual installation after downloading. 

To download the iHVI toolkit : 

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

## Technical documentation

Refer to [iHVI User Manual](Documentation.md) for more detailed explanation on iHVI operation


