#  ____________________________________________________________________
#                                                                       
#  Written by Alex Abair, 2026                                          
#                                                                       
#  This is an experiment to explore trends in Chaiturus marrubiastrum  
#  distribution based entirely on iNaturalist records.                  
#                                                                       
#  Future work to fold in herbarium records may be useful, but I don't 
#  believe that it's well-represented in specimens from North America  
#  ____________________________________________________________________

from pathlib import Path
import requests
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from pyproj import Transformer

OUTPUT = Path("chaiturus_output")
OUTPUT.mkdir(exist_ok=True)
CSV = OUTPUT / "observations_2004_2026.csv"

FPS = 15 # The optimal speed is subjective and variable by taxon
STEPS = 4
WIDTH, HEIGHT = 1080, 1920

# Reuse previously downloaded observations so as not to burden iNat
if not CSV.exists():
    raise FileNotFoundError(
        f"Missing {CSV}. Run your previous script "
        "once to download observations."
    )

df = pd.read_csv(CSV)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date", "lon", "lat"]).copy()
df = df[
    (df.date >= "2004-01-01") &
    (df.date <= "2026-09-30")
]
df["month"] = df.date.dt.to_period("M")
df = df.sort_values("date").reset_index(drop=True)

if df.empty:
    raise ValueError("No dated observations in CSV.")
#  _____________________
# |                     |
# |      MAP DATA       |
# |_____________________|

def load_map(filename, url):
    path = OUTPUT / filename
    if not path.exists():
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        path.write_bytes(response.content)
    return gpd.read_file(
        "zip://" + str(path.resolve())
    )

# Use polygon boundaries.

states = load_map(
    "states_polygons_10m.zip",
    "https://naturalearth.s3.amazonaws.com/"
    "10m_cultural/"
    "ne_10m_admin_1_states_provinces.zip"
)

countries = load_map(
    "countries_50m_v3.zip",
    "https://naturalearth.s3.amazonaws.com/"
    "50m_cultural/"
    "ne_50m_admin_0_countries.zip"
)

lakes = load_map(
    "lakes_50m_v3.zip",
    "https://naturalearth.s3.amazonaws.com/"
    "50m_physical/ne_50m_lakes.zip"
)

#  _______________________
# |                       |
# |  PROJECT COORDINATES  |
# |_______________________|

crs = "EPSG:5070"
trans = Transformer.from_crs(
    "EPSG:4326", crs, always_xy=True
)

df["x"], df["y"] = trans.transform(
    df.lon.to_numpy(),
    df.lat.to_numpy()
)

# Concentrate on eastern North America where Chaiturus has been spreading
east = df[
    (df.lon >= -100) &
    (df.lon <= -65) &
    (df.lat >= 25) &
    (df.lat <= 55)
]

if east.empty:
    east = df

left, right = np.quantile(
    east.x, [0.01, 0.99]
)
bottom, top = np.quantile(
    east.y, [0.01, 0.99]
)

# Guarantee Michigan is included. I don't know why Michigan was giving me trouble...
mx, my = trans.transform(
    [-90.5, -82.0],
    [41.5, 47.8]
)

left = min(left, min(mx))
right = max(right, max(mx))
bottom = min(bottom, min(my))
top = max(top, max(my))

# Add padding and force portrait framing
cx = (left + right) / 2
cy = (bottom + top) / 2

w = (right - left) * 1.17
h = (top - bottom) * 1.17

map_ratio = 0.58
h = max(h, w / map_ratio)
w = h * map_ratio

bounds = (
    cx - w / 2,
    cx + w / 2,
    cy - h / 2,
    cy + h / 2
)

def prepare(gdf):
    return gdf.to_crs(crs).cx[
        bounds[0]:bounds[1],
        bounds[2]:bounds[3]
    ]

states = prepare(states)
countries = prepare(countries)
lakes = prepare(lakes)

#  _______________________
# |                       |
# |  BUILD VERTICAL MAP   |
# |_______________________|

fig = plt.figure(
    figsize=(WIDTH / 100, HEIGHT / 100),
    dpi=100,
    facecolor="#101820"
)

ax = fig.add_axes(
    [0.035, 0.14, 0.93, 0.76]
)
ax.set_facecolor("#101820")

countries.plot(
    ax=ax,
    facecolor="#23363b",
    edgecolor="#6a7b80",
    linewidth=0.6,
    zorder=1
)

states.plot(
    ax=ax,
    facecolor="none",
    edgecolor="#536a70",
    linewidth=0.5,
    zorder=2
)

lakes.plot(
    ax=ax,
    facecolor="#101820",
    edgecolor="#6a7b80",
    linewidth=0.35,
    zorder=3
)

ax.set_xlim(bounds[0], bounds[1])
ax.set_ylim(bounds[2], bounds[3])
ax.set_aspect("equal")
ax.axis("off")

fig.text(
    0.5, 0.945,
    "Chaiturus marrubiastrum",
    color="white",
    fontsize=24,
    fontstyle="italic",
    ha="center"
)

fig.text(
    0.5, 0.917,
    "iNaturalist observations · 2004–2026",
    color="#9db8b7",
    fontsize=15,
    ha="center"
)

date_label = fig.text(
    0.5, 0.088, "",
    color="white",
    fontsize=28,
    ha="center"
)

count_label = fig.text(
    0.5, 0.062, "",
    color="#9db8b7",
    fontsize=16,
    ha="center"
)

old_scatter = ax.scatter(
    [], [],
    s=45,
    c="#65d6c1",
    alpha=0.8,
    edgecolors="none",
    zorder=5
)

new_scatter = ax.scatter(
    [], [],
    s=66,
    c="#f5cf65",
    alpha=0,
    edgecolors="none",
    zorder=6
)

def offsets(part):
    return part[["x", "y"]].to_numpy().reshape(-1, 2)

def frame(writer):
    fig.canvas.draw()
    image = np.asarray(
        fig.canvas.buffer_rgba()
    )[:, :, :3].copy()
    writer.append_data(image)

#  ___________________________________
# |                                   |
# |  RENDER MONTHS WITH OBSERVATIONS  |
# |___________________________________|

video = OUTPUT / "chaiturus_spread_vertical_v3.mp4"
months = sorted(df.month.unique())

with imageio.get_writer(
    video,
    fps=FPS,
    codec="libx264",
    quality=8,
    macro_block_size=1
) as writer:

    for month in months:
        older = df[df.month < month]
        current = df[df.month == month]

        old_scatter.set_offsets(
            offsets(older)
        )
        new_scatter.set_offsets(
            offsets(current)
        )

        date_label.set_text(
            month.strftime("%B %Y")
        )
        count_label.set_text(
            f"{len(older) + len(current):,} observations"
        )

        for step in range(STEPS):
            new_scatter.set_alpha(
                (step + 1) / STEPS
            )
            frame(writer)

        print("Rendered", month)

    #  ___________________________
    # |                           |
    # |    FINAL THREE PULSES     |
    # |___________________________|

    old_scatter.set_offsets(
        offsets(df)
    )
    new_scatter.set_offsets(
        np.empty((0, 2))
    )
    new_scatter.set_alpha(0)

    for cycle in range(3):
        opacities = np.concatenate((
            np.linspace(0.8, 0, 12),
            np.linspace(0, 0.8, 12)
        ))

        for opacity in opacities:
            old_scatter.set_alpha(
                float(opacity)
            )
            frame(writer)

    # Hold final map for one second
    for _ in range(FPS):
        frame(writer)

plt.close(fig)
print("Finished:", video)
