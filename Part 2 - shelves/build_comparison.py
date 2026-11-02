"""Validate saved detections, export counts, and build an offline comparison page.
No inference calls are made: the source files preserve interactive ChatGPT and
user-operated Roboflow results. Run: python build_comparison.py
"""
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


def load_data():
    llm = json.loads((BASE/'results/llm_response.json').read_text())
    cv = json.loads((BASE/'results/roboflow_browser.json').read_text())
    lmap = {i['image']: i for i in llm['images']}
    cmap = {i['image']: i for i in cv['images']}
    expected = {p.relative_to(BASE).as_posix() for p in BASE.glob('zone*/*.jpg')}
    if len(lmap) != len(llm['images']) or len(cmap) != len(cv['images']):
        raise ValueError('Duplicate image records')
    if set(lmap) != expected or set(cmap) != expected or len(expected) != 7:
        raise ValueError('Both methods must contain exactly the seven supplied images')
    images = []
    for filename in sorted(expected):
        left, right = lmap[filename], cmap[filename]
        if (left['width'],left['height'],right['width'],right['height']) != (640,640,640,640):
            raise ValueError('Unexpected image dimensions')
        for b in left['boxes']:
            if not (0 <= b['x1'] < b['x2'] <= 640 and 0 <= b['y1'] < b['y2'] <= 640):
                raise ValueError('Invalid LLM bounding box')
        boxes = []
        for b in right['predictions']:
            if b['class'] != 'Empty-space' or not (.25 <= b['confidence'] <= 1):
                raise ValueError('Unexpected class or below-threshold prediction')
            x1,y1 = b['x']-b['width']/2,b['y']-b['height']/2
            x2,y2 = x1+b['width'],y1+b['height']
            if not (0 <= x1 < x2 <= 640 and 0 <= y1 < y2 <= 640):
                raise ValueError('Invalid specialized-model bounding box')
            boxes.append(dict(x1=x1,y1=y1,x2=x2,y2=y2,confidence=b['confidence']))
        images.append(dict(image=filename,zone=filename.split('/')[0],name=filename.split('WA')[1][:4],llm=left['boxes'],cv=boxes))
    return images


def main():
    images=load_data()
    with (BASE/'results/comparison.csv').open('w', newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['zone','filename','llm_empty_areas','specialized_empty_areas','specialized_minus_llm'])
        for i in images:
            writer.writerow([i['zone'],Path(i['image']).name,len(i['llm']),len(i['cv']),len(i['cv'])-len(i['llm'])])
    template=(BASE/'comparison_template.html').read_text()
    payload=json.dumps(images).replace('<','\\u003c')
    (BASE/'comparison.html').write_text(template.replace('/*DATA*/[]',payload))
    print('Created comparison.html and results/comparison.csv')
    print('LLM total:',sum(len(i['llm']) for i in images))
    print('Specialized total:',sum(len(i['cv']) for i in images))


if __name__ == '__main__':
    main()
