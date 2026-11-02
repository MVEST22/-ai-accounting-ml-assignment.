"""Optional API rerun of the specialized model; NOT the source of saved browser results.
Install: python -m pip install "inference-sdk>=0.64"
Set ROBOFLOW_API_KEY locally, then: python run_roboflow.py
Uses the account's inference allowance; verify availability before running.
Never put the key in GitHub. API results are saved separately from browser evidence.
"""
import json
import os
from pathlib import Path


def main():
    key=os.environ.get('ROBOFLOW_API_KEY')
    if not key:
        raise SystemExit('Set ROBOFLOW_API_KEY locally before running; do not paste it in chat or commit it.')
    from inference_sdk import InferenceConfiguration, InferenceHTTPClient
    base=Path(__file__).resolve().parent
    client=InferenceHTTPClient(api_url='https://serverless.roboflow.com',api_key=key)
    client.configure(InferenceConfiguration(confidence_threshold=0.25,iou_threshold=0.5,api_key_transport='header'))
    out=base/'results/api_rerun'
    out.mkdir(parents=True,exist_ok=True)
    for path in sorted(base.glob('zone*/*.jpg')):
        # Fail normally on API errors; never replace a failed request with zero detections.
        result=client.infer(str(path),model_id='empty-shelf-detection-r8cfz/1')
        (out/(path.stem+'.json')).write_text(json.dumps(result,indent=2)+'\n')
        print(path.name,len(result['predictions']))


if __name__ == '__main__':
    main()
