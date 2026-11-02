# Part 2: How many items are missing from the shelves?

A retailer wants to give employees better information about empty shelf spaces so that products can be replenished quickly. Photographs of store shelves can be analyzed to identify missing items, compare store zones, and help employees decide where restocking is needed most.

## Task

Using all the shelf photographs in the zone folders:

1. Use an LLM to identify and count the missing items in each image. Ask the LLM to return the location of every detected missing area as a bounding box or polygon so that the detections can be drawn over the image.
2. Find a suitable specialized computer-vision model on [Roboflow Universe](https://universe.roboflow.com/) and use it to identify and count the missing items in each image. 
3. Build a comparison webpage on your own computer. The webpage must display every image with an LLM overlay and a specialized-model overlay so that you can compare the counts and visually assess the accuracy of the two methods. The webpage only needs to run locally and does not need to be published online.

## Deliverables

Submit:

- A table comparing the LLM and specialized-model counts for every image.
- The code used to obtain the LLM detections.
- The code used for the specialized-model detections.
- A screenshot of the local comparison webpage showing the LLM and specialized-model overlays.
- A brief recommendation explaining which results should be shown to store employees.
