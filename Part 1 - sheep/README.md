# Part 1 — sheep counting

## Results so far

| Method | Count | Status |
|---|---:|---|
| Initial LLM visual estimate | Approximately 2,500 | Rough, unverified estimate from the conversation |
| LLM-generated Python script | 3,621 | Executed on the supplied photograph; unvalidated heuristic |
| CountThings | Pending | Must be run and documented with a screenshot |

## Run the script

Install Python, then from this directory run:

```sh
python -m pip install -r requirements.txt
python count_sheep.py
```

No API key is needed. The script creates `results/summary.json`, `results/detections.csv`, `results/sensitivity.csv`, and `results/overlay.svg`. Open the SVG in a browser while keeping it in the results folder so the photograph resolves correctly. Coordinates use the original image size of 1942 × 1949 pixels.

## Method and limitations

The script detects locally bright regions, removes small regions, and suppresses nearby peaks. It is classical image processing, not a trained sheep-recognition model. The brightness and distance parameters were adjusted after an initial run visibly detected too many ground features. They were not calibrated against a known true count.

Visual inspection of the final overlay still shows false detections on terrain and possible missed or split sheep. Across nine parameter combinations, the counts ranged from 3,067 to 4,235. This is sensitivity to settings, not a confidence interval. The script count is reproducible but is not verified.

## Can I report this number to my audit partner?

You can report it as a preliminary AI estimate, clearly explaining its limitations. You should not present it as a verified livestock count or sufficient audit evidence. The sheep are small, closely grouped, and sometimes overlapping, so omissions and double counting are possible. The count needs independent validation, and the photograph's date, completeness, and connection to the farm must also be established.

## Remaining steps

1. Count the original photograph using CountThings and retain the original output screenshot.
2. Record any manual corrections and the final CountThings count.
3. Compare the overlays and investigate disagreement before choosing a number to report. Agreement alone does not establish accuracy.
4. Complete the class results form linked in the original instructions once all results are available.

At present, neither available number should be reported as a verified count. The final recommendation and confidence assessment remain pending independent checking and the CountThings result.
