***Chaiturus marrubiastrum* - Spread Across North America**

An animated visualization of the geographic accumulation of *Chaiturus
marrubiastrum* observations in North America, using georeferenced
records from <u>[iNaturalist](https://www.inaturalist.org/)</u>.\
The animation follows observations from January 2004 through September
2026, illustrating changes in the documented distribution of this
species over time.

**Overview**

This project uses Python to retrieve, process, and visualize iNaturalist
occurrence records. Observations are plotted cumulatively on a map of
eastern North America, with new records appearing as the animation
progresses.\
The visualization is designed for vertical video platforms, including
Instagram Reels, TikTok, and YouTube Shorts.

**Visualization features**

- Temporal coverage: January 2004 - September 2026

- **Data source:** iNaturalist observations API

- **Geographic coverage:** Eastern North America, including the United
  States and southern Canada

- **Temporal resolution:** Monthly, excluding months without
  observations

- **Animation:** 15 frames per second, with four interpolated frames per
  represented month

- **Format:** 1080 × 1920 pixels (9:16 aspect ratio)

- **Basemap:** Natural Earth country, state, province, and lake
  boundaries

- **Final sequence:** Three cycles of fading accumulated observation
  points in and out

Previously recorded observations remain visible as new records appear.
At the conclusion of the animation, all recorded points pulse three
times to emphasize the cumulative distribution.

**Interpretation**

This animation depicts the accumulation of documented occurrences,
rather than directly measuring the biological spread of *Chaiturus
marrubiastrum*.\
Several factors influence the geographic and temporal distribution of
iNaturalist observations:

- Changes in observer participation and geographic coverage

- Increased use of iNaturalist over time

- Variation in identification accuracy and research effort

- Delayed uploads of historical observations

- Differences between the dates of initial establishment and first
  documented occurrence

Consequently, newly appearing points should not necessarily be
interpreted as newly established populations.\
Months without observations are omitted from the animation, meaning that
elapsed video time is not proportional to elapsed calendar time.\
The map is cropped to emphasize eastern North America. Some records
outside the displayed extent may not be visible.

**Requirements**

- Python 3.10 or later

- requests

- pandas

- numpy

- matplotlib

- geopandas

- pyproj

- imageio

- imageio-ffmpeg

Install the dependencies:

    python -m pip install requests pandas numpy matplotlib geopandas pyproj imageio imageio-ffmpeg

A Python virtual environment is recommended.

**Usage**

Clone the repository:

    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
    cd YOUR_REPOSITORY

Run the visualization script:

    python chaiturus_spread_v3.py

The current script expects a previously downloaded observation dataset
at:

    chaiturus_output/observations_2004_2026.csv

If the CSV does not exist, first run the earlier data-download script or
supply a compatible CSV containing `id`, `date`, `lon`, and `lat`
columns.\
The script automatically downloads and caches Natural Earth boundary
datasets when needed.\
The finished video is saved to:

    chaiturus_output/chaiturus_spread_vertical_v3.mp4

**Animation design**

The animation distinguishes previously documented observations from
those recorded in the currently displayed month.

- **Turquoise points:** Previously recorded observations

- **Yellow points:** Observations from the displayed month, gradually
  fading into view

- **Dark background:** Geographic context with subdued political
  boundaries

Point sizes, colors, frame rate, and animation duration can be modified
directly in the Python script.\
The map uses the NAD83 / Conus Albers projection (EPSG:5070), which is
suitable for displaying the contiguous United States and surrounding
regions.

**Data and cartographic sources**

Observation data

<u>[iNaturalist](https://www.inaturalist.org/)</u> -
Community-contributed biodiversity observations retrieved through the
<u>[iNaturalist API](https://api.inaturalist.org/v1/docs/)</u>.\
Observation records retain their original iNaturalist identifiers.
Individual observation photographs and associated metadata may be
subject to separate licenses.

**Geographic boundaries**

<u>[Natural Earth](https://www.naturalearthdata.com/)</u> -
Public-domain geographic datasets used for country boundaries, state and
province polygons, and lakes.

**Limitations**

The visualization should be treated as an exploratory representation of
recorded occurrences rather than a formal reconstruction of invasion
history.\
The current workflow also has several technical limitations:

1.  The observation dataset is cached locally and is not automatically
    refreshed on subsequent runs.

2.  The original data-download workflow uses annual API queries, which
    may encounter iNaturalist's pagination limits if a year contains
    sufficiently many records.

3.  The geographic crop is optimized for eastern North America rather
    than the complete North American distribution.

4.  The animation does not correct for spatial or temporal variation in
    observation effort.

5.  Repeated observations from the same locality are displayed
    independently rather than being consolidated into unique
    populations.

**Related project**

<u>[Lamium
Phenology](https://github.com/AlexanderAbair/Lamium_phenology)</u> - An
earlier visualization project exploring the seasonal distribution of
*Lamium* observations using iNaturalist data.\
Whereas the *Lamium* project visualizes phenological patterns, this
project explores changes in the documented geographic distribution of a
species over time.

**Author**

Alex Abair\
Botany, biodiversity informatics, and scientific visualization.

**Acknowledgments**

Observation data contributed by the iNaturalist community. Geographic
data provided by Natural Earth.
