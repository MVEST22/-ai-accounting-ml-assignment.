"""Count bright sheep-like regions; heuristic estimate, not a trained detector.
Run: python count_sheep.py
Dependencies: numpy scipy Pillow
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def detect(gray, threshold, min_distance):
    # Sheep are brighter than their immediate background. Remove broad terrain variation.
    smooth = ndi.gaussian_filter(gray, sigma=1)
    contrast = smooth - ndi.grey_opening(smooth, size=(19, 19))
    mask = (contrast > threshold) & (smooth > 155)
    labels, _ = ndi.label(mask)
    sizes = np.bincount(labels.ravel())
    mask &= sizes[labels] >= 12
    score = ndi.gaussian_filter(np.where(mask, contrast, 0), sigma=1)
    peaks = (score == ndi.maximum_filter(score, size=5)) & mask
    candidates = np.argwhere(peaks)
    candidates = sorted(candidates, key=lambda p: float(score[tuple(p)]), reverse=True)
    accepted = []
    occupied = np.zeros(gray.shape, dtype=bool)
    for y, x in candidates:
        if occupied[y, x]:
            continue
        accepted.append((int(x), int(y)))
        y0, y1 = max(0, y-min_distance), min(gray.shape[0], y+min_distance+1)
        x0, x1 = max(0, x-min_distance), min(gray.shape[1], x+min_distance+1)
        yy, xx = np.ogrid[y0:y1, x0:x1]
        occupied[y0:y1, x0:x1] |= (yy-y)**2+(xx-x)**2 <= min_distance**2
    return sorted(accepted, key=lambda p: (p[1], p[0]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', nargs='?', type=Path, default=Path(__file__).parent/'Innovation_mindset_case_studies_Bryans_Amazing_Animals.jpg')
    parser.add_argument('--threshold', type=float, default=40)
    parser.add_argument('--min-distance', type=int, default=12)
    args = parser.parse_args()
    if args.threshold <= 0 or args.min_distance < 1:
        parser.error('threshold must be positive and min-distance at least 1')
    im = Image.open(args.image).convert('RGB')
    gray = np.asarray(im.convert('L'), dtype=np.float32)
    points = detect(gray, args.threshold, args.min_distance)
    out = Path(__file__).parent/'results'
    out.mkdir(exist_ok=True)
    with (out/'detections.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'x', 'y'])
        writer.writerows((i, x, y) for i, (x, y) in enumerate(points, 1))
    from html import escape
    circles = ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="none" stroke="#ff3030" stroke-width="1.5"/>' for x,y in points)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{im.width}" height="{im.height}" viewBox="0 0 {im.width} {im.height}"><image href="../{escape(args.image.name, quote=True)}" width="{im.width}" height="{im.height}"/>{circles}</svg>'
    (out/'overlay.svg').write_text(svg)
    summary = {'count': len(points), 'method': 'brightness contrast and local maxima with distance suppression', 'threshold':args.threshold, 'min_distance':args.min_distance, 'image_size':list(im.size), 'image_sha256':hashlib.sha256(args.image.read_bytes()).hexdigest(), 'status':'unvalidated heuristic estimate; detections may include rocks or split/merge sheep'}
    (out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    with (out/'sensitivity.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['contrast_threshold','min_distance','count'])
        for threshold in [30,40,50]:
            for distance in [10,12,14]:
                writer.writerow([threshold,distance,len(detect(gray,threshold,distance))])
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
