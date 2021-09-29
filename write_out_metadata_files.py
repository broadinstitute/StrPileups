import collections
import json
import math
import pandas as pd

COLORS = {
    "normal": "#00AA00",
    "intermediate": "#FFCC00",
    "full-expansion": "#AA0000",
    "double-expansion": "#AA00CC",
}

NUM_ANALYSTS = 12

df = pd.read_table("./Table-S1.tsv")
for _, row in df.iterrows():
    sample_id = row["Sample"]
    output_path = f"images/{sample_id}/flipbook_metadata.json"
    with open(output_path, "wt") as f:
        flipbook_metadata = {
            "Locus_(Inheritance)": "<span style='color: #1133FF; white-space:nowrap'><b>" + row["Locus"] + "</b></span>",
        }
        for key in "Sex", "PCR_verdict", "EH_verdict":
            if row[key]:
                flipbook_metadata[key] = row[key]
            else:
                flipbook_metadata[key] = ""

        analyst_response_counter = collections.Counter([row[f"Analyst{i}"] for i in range(1, NUM_ANALYSTS + 1)])
        analyst_response_counter_sorted = sorted(analyst_response_counter.items(),  key=lambda t: -t[1])
        flipbook_metadata["MostCommonAnalystResponse"] = analyst_response_counter_sorted[0][0]
        flipbook_metadata["NumAnalystsMatchedPcr"] = sum([1 if row[f"Analyst{i}"] == row["PCR_verdict"] else 0 for i in range(1, NUM_ANALYSTS + 1)])

        if not math.isnan(row["Premutation"]):
            flipbook_metadata["Premutation_[&gt;]"] = int(row["Premutation"])
        if not math.isnan(row["Pathogenic"]):
            flipbook_metadata["Pathogenic_[&GreaterEqual;]"] = int(row["Pathogenic"])

        for key in "PCR_short", "PCR_long", "EH_short", "EH_short_CI", "EH_long", "EH_long_CI":
            flipbook_metadata[key] = row[key]
            if not row[key] or (isinstance(row[key], float) and math.isnan(row[key])):
                flipbook_metadata[key] = ""
            elif isinstance(row[key], float):
                flipbook_metadata[key] = int(row[key])

        flipbook_metadata["EH_matched_PCR"] = "Yes" if row["PCR_verdict"] == row["EH_verdict"] else "No"
        for key in "PCR_verdict", "EH_verdict", "MostCommonAnalystResponse":
            flipbook_metadata[key] = (
                f"<span style='color: {COLORS.get(flipbook_metadata[key])}; white-space:nowrap'><b>" 
                f"{flipbook_metadata[key]}"
                f"</b></span>"
            )
        json.dump(flipbook_metadata, f)
        print(f"Wrote {output_path}")

print("Done")