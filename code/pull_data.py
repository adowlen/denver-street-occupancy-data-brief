"""Pull the full Denver street occupancy permits layer.

Source (City and County of Denver open data, ArcGIS FeatureServer):
ODC_DEV_STREETOCCUPANCYPPERMITS_L layer 297 - street occupancy permits
extracted from the Accela permit database by DOTI, processed daily by
Technology Services GIS. Includes expired, currently active, and future
scheduled permits. One permit may span multiple street segments (one
row per segment-closure record in this layer).

Paginated attribute pull (returnGeometry=false; Shape__Length is a
stored attribute). Saved to data/permits_raw.parquet + a CSV copy.
Server-side counters in data/raw_aggregates.json; pull record in
data/pull_log.json. Asserts pulled == server count.
"""
import json, pathlib
import urllib.parse, urllib.request

import pandas as pd

HOST = "https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services"
LAYER = f"{HOST}/ODC_DEV_STREETOCCUPANCYPPERMITS_L/FeatureServer/297"
PAGE = 2000
HERE = pathlib.Path(__file__).resolve().parent.parent
DATA = HERE / "data"


def q(url, params):
    full = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(full, headers={"User-Agent": "MachineReadable pull"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())


def count(base, where="1=1"):
    return q(base + "/query", {"where": where, "returnCountOnly": "true", "f": "json"})["count"]


def group(base, field, where="1=1", limit=5000):
    d = q(base + "/query",
          {"where": where, "groupByFieldsForStatistics": field,
           "outStatistics": json.dumps([{"statisticType": "count",
                                         "onStatisticField": "OBJECTID",
                                         "outStatisticFieldName": "cnt"}]),
           "orderByFields": "cnt DESC", "resultRecordCount": limit, "f": "json"})
    return [[f["attributes"][field], f["attributes"]["cnt"]]
            for f in d.get("features", [])]


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    meta = q(LAYER, {"f": "json"})
    server_count = count(LAYER)
    rows, offset = [], 0
    while True:
        d = q(LAYER + "/query",
              {"where": "1=1", "outFields": "*", "returnGeometry": "false",
               "orderByFields": "OBJECTID", "resultOffset": offset,
               "resultRecordCount": PAGE, "f": "json"})
        feats = d.get("features", [])
        rows.extend(f["attributes"] for f in feats)
        if len(feats) < PAGE:
            break
        offset += PAGE
    assert len(rows) == server_count, (len(rows), server_count)
    df = pd.DataFrame(rows)
    df.to_parquet(DATA / "permits_raw.parquet", index=False)
    df.to_csv(DATA / "permits_raw.csv", index=False)
    aggregates = {
        "server_count": server_count,
        "purpose_counter": group(LAYER, "PURPOSE"),
        "exempt_counter": group(LAYER, "EXEMPT"),
        "asit_type_counter": group(LAYER, "ASIT_TYPE"),
        "gis_load_type_counter": group(LAYER, "GIS_LOAD_TYPE"),
        "company_counter_top100": group(LAYER, "COMPANY", limit=100),
    }
    (DATA / "raw_aggregates.json").write_text(json.dumps(aggregates, indent=1))
    log = {
        "pull_date": "2026-10-30",
        "layer": LAYER,
        "layer_name": meta.get("name"),
        "description": meta.get("description"),
        "editingInfo": meta.get("editingInfo"),
        "server_count": server_count,
        "pulled_rows": len(rows),
        "fields": [f["name"] for f in meta.get("fields", [])],
    }
    (DATA / "pull_log.json").write_text(json.dumps(log, indent=1))
    print(json.dumps({"server_count": server_count, "pulled": len(rows)}, indent=1))


if __name__ == "__main__":
    main()
