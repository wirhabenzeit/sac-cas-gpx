# SAC/CAS route download

This script downloads SAC/CAS routes in `gpx` format. 

## Usage Guide
Requires 
* `python3`
* libraries `pyproj`, `gpxpy`, `json`, `requests`, `argparse`, `browser_cookie3`
* SAC/CAS membership and `Google Chrome` for member-only routes (cookie information is used)

```
python3 sac_to_gpx.py route_ID [--lang de/en/fr/it]
```

The `route_ID` is the last part of the URL, e.g. `207` for `https://www.sac-cas.ch/en/huts-and-tours/sac-route-portal/medelserhuette-sac-2147000168/mountain-hiking/from-curaglia-via-val-plattas-207/`