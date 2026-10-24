# City Brain: public datasets explained

One Jupyter notebook per public dataset the **City Brain** uses (detection, graph DB, mock sensors, scenarios, evaluation, scoring). Each notebook explains:

1. **What's inside**: the source, the licence, the columns and what they mean, the first rows.
2. **What it shows**: short analyses and plots on the real data.
3. **How it helps the City Brain**: detection rules, graph, mock, scenarios, evaluation and scoring, with the limits.

The notebooks are already executed, so you can **read them directly on GitHub** without installing anything.

## The notebooks

| # | Notebook | Domain | Utility | Data in repo? |
|---|---|---|---|---|
| 01 | [UTD19 urban loop detectors (Torino)](notebooks/01_utd19_traffic_loop_detectors.ipynb) | Traffic | Very high | No (academic licence) |
| 02 | [NYC FloodNet street flood sensors](notebooks/02_nyc_floodnet_street_flood_sensors.ipynb) | Flood | High | Yes |
| 03 | [USGS Raritan River gauge (2021)](notebooks/03_usgs_raritan_river_gauge.ipynb) | Flood | High | Yes |
| 04 | [UCI ElectricityLoadDiagrams](notebooks/04_uci_electricity_load.ipynb) | Power | High | Sample (2013) |
| 05 | [NYC 311 calls, Hurricane Ida night](notebooks/05_nyc_311_calls_ida_night.ipynb) | Calls | Very high | Yes |
| 06 | [NYC Motor Vehicle Collisions](notebooks/06_nyc_motor_vehicle_collisions.ipynb) | Accidents | High | Yes |
| 07 | [NYC DOT Traffic Speeds](notebooks/07_nyc_dot_traffic_speeds.ipynb) | Traffic | High | Yes |
| 08 | [DOE Eagle-I power outages](notebooks/08_doe_eaglei_power_outages.ipynb) | Power | High | Sample (Aug–Sep 2021) |
| 09 | [EPA AirNow wildfire smoke](notebooks/09_epa_airnow_wildfire_smoke.ipynb) | Air quality | High | Sample (NY + NJ) |
| 10 | [NIST smoke alarm tests: fires vs cooking](notebooks/10_nist_smoke_alarm_fire_tests.ipynb) | Fire sensors | Very high | Yes |
| 11 | [Fire & Smoke Twin fire calls](notebooks/11_fire_and_smoke_twin_fire_calls.ipynb) | Fire calls | Medium | No |
| 12 | [FARS 2024 fatal crashes](notebooks/12_fars_2024_fatal_crashes.ipynb) | Accidents | Medium | Sample (accident table) |
| 13 | [SmartGrid cyber-physical attacks](notebooks/13_smartgrid_cyber_physical_attacks.ipynb) | Power / security | Medium | No (IEEE terms) |
| 14 | [Intel Berkeley Lab sensor faults](notebooks/14_intel_lab_sensor_faults.ipynb) | Sensor faults | High | Sample (8 motes) |
| 15 | [Numenta Anomaly Benchmark](notebooks/15_nab_anomaly_benchmark.ipynb) | Evaluation | Medium | Sample |

**Where to start:** notebooks 01, 05 and 10 have the most important lessons. Notebooks 02, 03, 05, 06, 07 and 08 together describe the same real storm (Hurricane Ida, 1–2 Sep 2021), which is the basis of the "Storm night" demo scenario.

## What the data taught us

1. **Signals with a daily rhythm need a per-sensor, per-hour, weekday/weekend baseline**, not a plain moving average (01, 04, 15).
2. **Never open an incident on one sensor**: dying batteries fake 385 °C (14), and a single traffic detector's speed drop is noise (01).
3. **Every incident type needs a second signal.** For fire, it's a **CO rise**: 30/30 fires vs 0/60 cooking tests (10). For floods, calls and sensors agree within minutes (05).
4. **Silence and speed 0 are ambiguous**, not incidents (07, 14).
5. **A city-wide rise with no call is regional**, e.g. wildfire smoke rather than a fire (09).
6. **Fake readings** look like a sudden step on a few devices while the network looks normal (13).

## Run the notebooks yourself

```bash
git clone <this repo> && cd city-brain-notebooks
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/
```

Notebooks marked "Yes" or "Sample" run straight away on `data/`. For the others, download the dataset (each notebook's header says where), keep the folder layout used in the notebook (for example `traffic/utd19/torino.csv`), and point to it:

```bash
export CITY_BRAIN_DATA=/path/to/your/datasets
```

`cbdata.path()` looks in `data/` first, then in `$CITY_BRAIN_DATA`. `tools/make_samples.py` shows exactly how the samples were cut from the full downloads.

## Licences and citations

The **code** in this repo can be reused freely. The **data samples** keep their original licences:

| Dataset | Terms |
|---|---|
| NYC Open Data (FloodNet, 311, Collisions, DOT speeds) | Open; acknowledge NYC Open Data and the FloodNet project |
| USGS NWIS, EPA AirNow, FARS (NHTSA), NIST | US government works, public; acknowledge the agency. NIST: cite TN 1947, DOI 10.18434/T4530X |
| UCI ElectricityLoadDiagrams | CC BY 4.0; cite the UCI dataset (id 321) |
| DOE Eagle-I | CC BY 4.0; cite DOI 10.6084/m9.figshare.24237376 |
| Intel Berkeley Lab | Open; acknowledge Intel Research Berkeley / MIT CSAIL |
| NAB | MIT (`data/anomaly-benchmark/nab/LICENSE.txt`); cite Ahmad et al. (2017) |
| UTD19 (not included) | Academic / non-commercial; cite Loder et al. (2019), *Scientific Reports* 9 |
| SmartGrid attack set (not included) | IEEE DataPort terms; DOI 10.21227/symr-bz19 |
| Fire & Smoke Twin calls (not included) | See the repository; cite arXiv:2305.18313 |
