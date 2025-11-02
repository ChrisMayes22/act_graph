# lr_errors_by_type_pie_readable.py
# Pie of ERRORS by type with larger numbers and a readable color palette.

import json
import matplotlib.pyplot as plt
import numpy as np

# ---- Edit your data here (errors-only schema) ----
data_json = r"""
{
  "errors": [
    { "type": "Detail", "errors": 6 },
    { "type": "New Information", "errors": 2 },
    { "type": "Trend", "errors": 2 }
  ]
}
"""
TITLE = "Errors by Type"
COLORMAP_NAME = "Set2"         # try: "Set2", "tab10", or "Pastel1"
NUMBER_FONTSIZE = 14
LEGEND_FONTSIZE = 11
# --------------------------------------------------


def load_data(json_str):
    data = json.loads(json_str)
    rows = [r for r in data.get("errors", []) if int(r.get("errors", 0)) > 0]
    rows.sort(key=lambda r: (-int(r["errors"]), r["type"]))
    labels = [r["type"] for r in rows]
    counts = [int(r["errors"]) for r in rows]
    return labels, counts

def main():
    labels, counts = load_data(data_json)
    if not counts:
        print("No errors to display.")
        return

    total_errors = sum(counts)
    cmap = plt.get_cmap(COLORMAP_NAME)
    # Pick as many colors as we need from the colormap
    colors = cmap(np.linspace(0, 1, len(labels)))

    def autopct_counts(pct):
        count = int(round(pct * total_errors / 100.0))
        return f"{count}" if count > 0 else ""

    fig, ax = plt.subplots(figsize=(8.5, 6))
    fig.subplots_adjust(right=0.8)

    wedges, texts, autotexts = ax.pie(
        counts,
        colors=colors,
        startangle=90, counterclock=False,
        autopct=autopct_counts,
        pctdistance=0.68,                 # numbers inside the slice
        textprops={"fontsize": NUMBER_FONTSIZE},
        wedgeprops={"linewidth": 1.2, "edgecolor": "white"}
    )

    # Ensure number labels use the requested fontsize (textprops already sets it, but be explicit)
    for t in autotexts:
        t.set_fontsize(NUMBER_FONTSIZE)

    ax.axis("equal")
    ax.set_title(TITLE)

    ax.legend(
        wedges, labels,
        title="Error type",
        loc="center left", bbox_to_anchor=(1.02, 0.5),
        fontsize=LEGEND_FONTSIZE, title_fontsize=LEGEND_FONTSIZE
    )

    fig.text(0.015, 0.015, f"Total errors: {total_errors}",
             ha="left", va="bottom", fontsize=11)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()