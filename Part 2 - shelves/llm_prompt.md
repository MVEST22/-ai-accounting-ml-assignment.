# Task applied to the interactive LLM visual assessment

Inspect every supplied shelf photograph. Identify visible contiguous empty front-facing shelf areas that suggest a need for replenishment. Count each area once, rather than guessing how many individual products would fit inside it. Exclude floor, black image borders, normal shelf edges, and small ordinary spacing between stocked products. Return the image filename and approximate axis-aligned bounding boxes, with a short reason for each detection. Use original 640 × 640 pixel coordinates, with x1/y1 at the top-left and x2/y2 at the bottom-right. Treat recessed stock with exposed shelf front as potentially needing replenishment, and retain uncertainty about whether a gap is truly empty.

This documents the task interpretation used by ChatGPT in the conversation; it is not a transcript of a separately executed API request. The original assignment instructions are in `Part 2 - shelves.md`.

The structured visual response is preserved in `results/llm_response.json`, and the capture/replay code is `prepare_detections.py`. These are approximate model annotations and have not been validated against independently labelled ground truth. Box placement was produced after the specialized results were available.
