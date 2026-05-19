# Carbary auroral boundaries model

## Description

This python package conatins auroral oval model, developed by Carbary J. F. (2005). 

The statistical model allows calculation of the auroral boundaries at most MLTs as a function of Kp and can serve as an approximation to the shape and extent of the statistical oval. 
The model take Kp geomagnetic index and magnetic local time (mlt) as input and produce the peak, poleward and equatorward boundaries of the auroral oval.

Implements the Model, described in the original Carbary J. F. publication "A Kp-based model of auroral boundaries" (SPACE WEATHER, VOL. 3, S10001, doi:10.1029/2005SW000162, 2005)

Citation: Carbary, J. F. (2005), A Kp-based model of auroral boundaries, Space Weather, 3, S10001, doi:10.1029/2005SW000162.

***Python 3.10+ requires***

## Classes and Methods

Library provides **AuroralBoundary** class describing Auroral oval for using in python applications

### AuroralBoundary.intensity_map

The field contains Intensity in every point belongs the auroral oval.
Returns numpy ndarray of lists **[longitude, latitude, intense]**. 

## How to use

```python
from carbary_model import AuroralBoundary

boundary = AuroralBoundary(kp=5.2,
                           ut_hours=datetime.datetime.now(datetime.UTC).hour,
                           advanced_mode=True)

```
