# Carbary auroral boundaries model

## Description

Python implementation of the statistical Kp-based auroral oval model by **James F. Carbary (2005)**

Implements the Model, described in the original Carbary J. F. publication "A Kp-based model of auroral boundaries" (SPACE WEATHER, VOL. 3, S10001, doi:10.1029/2005SW000162, 2005)

> Citation: Carbary, J. F. (2005), A Kp-based model of auroral boundaries, Space Weather, 3, S10001, doi:10.1029/2005SW000162.
>
> https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2005SW000162

## What this package does

The statistical model allows calculation of the auroral boundaries at most MLTs as a function of `Kp` and can serve as an approximation to the shape and extent of the statistical oval. 
The model take Kp geomagnetic index and magnetic local time (mlt) as input and produce the peak, poleward and equatorward boundaries of the auroral oval.

The relations are linear:

```text
boundary(MLT) = C0(MLT) + C1(MLT) × Kp
```

Coefficients are taken directly from Tables 1–4 of the original paper.

## Model limitations

- Best performance for **Kp < 6**. At higher Kp the linear fits deteriorate.
- No reliable coefficients for several daytime MLT hours (roughly 9–13).
- The conversion from magnetic to geographic coordinates uses a simple tilted-dipole approximation.

## Requirements

- Python ≥ 3.10
- numpy

## Classes and Methods

Library provides **AuroralBoundary** class describing Auroral oval for using in python applications

### AuroralBoundary.intensity_map

The field contains Intensity in every point belongs the auroral oval.
Returns numpy ndarray of lists **[longitude, latitude, intensity]**.

## How to use

### Installation

```bash
pip install carbary_auroral_model
```

### Usage Example

```python
import datetime
from carbary_model import AuroralBoundary


current_date = datetime.datetime.now(datetime.UTC)
oval = AuroralBoundary(kp=5.2,
                       ut_hours=current_date.hour,
                       advanced_mode=True,
                       strict_mode=False,
                       smooth_mode=0)
data = {
    "time": current_date.strftime(format="%d-%m-%Y %H:%M"),
    "data": oval.intensity_map,
    "data_raw": oval.raw_intensity_map
}

```

### FYI

> Note on Coordinate Systems: Dynamic Geomagnetic Pole calculation via WMM Gauss coefficients was excluded from the 0.1.0 release. R&D validation confirmed that the default Magnetic Dip Pole framework yields more consistent results with the original Carbary (2005) model. The selection pole types code is preserved in the `feature/pole_variety_dev` branch for reference.
>
> The selection pole types feature included in 0.1.1.dev0 release
> 
> According R&D tests **running the model with `strict_mode=False` is preferred**
> 
> As established in J. Carbary's original 2005 paper, the raw satellite images from the Polar Ultraviolet Imager. Polar Ultraviolet Imager. The pixel locations were transformed to **Corrected Geomagnetic Latitude (CGM-MLAT)**  and magnetic local time (MLT).
> 
> https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2005SW000162
> 
> The CGM coordinates description:
> https://omniweb.gsfc.nasa.gov/vitmo/cgmm_des.html
> 
> Magnetic pole location:
> https://www.ncei.noaa.gov/products/wandering-geomagnetic-poles
> 
> Kp Index info:
> https://spaceweather.gfz-potsdam.de/products-data/forecasts/forecast-kp-index

## License
MIT License.
