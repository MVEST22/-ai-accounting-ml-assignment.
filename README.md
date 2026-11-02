# AI in Accounting — Machine Learning Assignment

This repository organizes the three parts of the ML assignment.

## Structure

- `Part 1 - sheep/`: sheep-counting instructions, counting script, results, and CountThings evidence.
- `Part 2 - shelves/`: shelf instructions, image detections, comparison webpage, and recommendation.
- `Part 3 - prediction/`: hotel cancellation instructions, Orange workflow, predictions, and dashboard.

## Current progress

- Original instructions added for all three parts.
- Initial LLM sheep estimate: approximately 2,500 (rough visual estimate, unverified).
- Sheep script executed: 3,621; CountThings export saved: 2,882. Comparison and provisional assessment documented; class form reported completed by the user. Counts remain provisional pending independent validation.
- Shelf comparison: seven images, LLM and user-run Roboflow outputs saved; offline webpage and counts table built. User-supplied local screenshot saved. A real seven-photo Qwen Colab run is saved separately (8 Qwen areas versus 47 saved Roboflow areas), with executed notebook, raw outputs, screenshots and reviewed recommendation. Roboflow used the free browser demo; see the Part 2 method limitation if both models must be run programmatically.
- Orange comparison completed by user: Random Forest selected (AUC 0.871). All 200 actual Orange predictions saved, validated and converted to CSV; standalone nightly dashboard built. Final Orange workflow and its screenshot saved; local dashboard summary and chart screenshots saved. All listed hotel deliverables are prepared.

## Source data

The sheep photograph, all seven shelf photographs, and `historical.csv` have been uploaded in their original folders.

## Submission evidence

Retain actual outputs and screenshots. Do not treat estimates, unrun code, or placeholder results as completed evidence. The shelf webpage runs locally; the hotel task specifically requires Orange Data Mining. Never commit API keys or passwords.

Part 2 evidence: completed Qwen inference, executed notebook and reviewed comparison are in `Part 2 - shelves/results/qwen_colab/`. Roboflow inference was performed in its browser demo and reused in the notebook, not executed through an API.
