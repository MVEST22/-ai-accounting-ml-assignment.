"""Build a dashboard from the user's actual Orange export, without retraining.
Run from any folder: python build_dashboard.py
Uses only the Python standard library. Each reservation is assumed to use one room.
"""
import calendar
import csv
import datetime as dt
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

BASE=Path(__file__).resolve().parent
CAPACITY=37


def read_orange(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        lines=list(csv.reader(f,delimiter='\t'))
    if len(lines)<4 or len(set(lines[0]))!=len(lines[0]):
        raise ValueError('Expected an Orange .tab export with three header rows')
    if any(len(row)!=len(lines[0]) for row in lines[3:]):
        raise ValueError('Malformed data row')
    return [dict(zip(lines[0],row)) for row in lines[3:]]


def main():
    rows=read_orange(BASE/'hotel_predictions.tab')
    with (BASE/'planned_reservations.csv').open(encoding='utf-8-sig',newline='') as f:
        planned=list(csv.DictReader(f))
    if len(rows)!=200 or len(planned)!=200:
        raise ValueError('Expected exactly 200 reservations in both sources')
    common=set(rows[0]) & set(planned[0])
    for i,(pred,original) in enumerate(zip(rows,planned),1):
        for field in common:
            if pred[field].strip()!=original[field].strip():
                raise ValueError(f'Original row alignment mismatch: row {i}, field {field}')
    daily=defaultdict(lambda:dict(bookings=0,expected=0.0))
    clean=[]
    for i,r in enumerate(rows,1):
        p=float(r['Random Forest (1)']);p0=float(r['Random Forest (0)'])
        if not (math.isfinite(p) and math.isfinite(p0) and 0<=p<=1 and 0<=p0<=1 and abs(p+p0-1)<1e-5):
            raise ValueError(f'Invalid probability at row {i}')
        arrival=dt.date(int(r['ArrivalDateYear']),list(calendar.month_name).index(r['ArrivalDateMonth'].strip()),int(r['ArrivalDateDayOfMonth']))
        nights=int(r['StaysInWeekendNights'])+int(r['StaysInWeekNights'])
        if nights<0:
            raise ValueError('Negative stay length')
        departure=arrival+dt.timedelta(days=nights)
        record={k:v for k,v in r.items() if k not in ['Selected','Random Forest','Random Forest (0)','Random Forest (1)']}
        record.update(ReservationID=i,ArrivalDate=arrival.isoformat(),DepartureDate=departure.isoformat(),Nights=nights,PredictedIsCanceled=int(r['Random Forest']),CancellationProbability=p,ShowProbability=p0)
        clean.append(record)
        # Include arrival night; exclude departure date. Zero-night stays occupy no nights.
        for d in range(nights):
            n=daily[(arrival+dt.timedelta(days=d)).isoformat()]
            n['bookings']+=1
            n['expected']+=1-p
    dates=[]
    if daily:
        day=dt.date.fromisoformat(min(daily))
        end=dt.date.fromisoformat(max(daily))
        while day<=end:
            key=day.isoformat();v=daily[key]
            dates.append(dict(date=key,bookings=v['bookings'],expected=v['expected'],capacity=CAPACITY,booked_headroom=CAPACITY-v['bookings'],expected_headroom=CAPACITY-v['expected']))
            day+=dt.timedelta(days=1)
    if not math.isclose(sum(i['expected'] for i in dates),sum(i['Nights']*(1-i['CancellationProbability']) for i in clean),abs_tol=1e-8):
        raise ValueError('Expected room-night reconciliation failed')
    if sum(i['bookings'] for i in dates)!=sum(i['Nights'] for i in clean):
        raise ValueError('Booked room-night reconciliation failed')
    out=BASE/'results';out.mkdir(exist_ok=True)
    def write_csv(path,records):
        with path.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    write_csv(BASE/'hotel_predictions.csv',clean)
    write_csv(out/'nightly_room_use.csv',dates)
    scores=[dict(model='Logistic Regression',AUC=.823,Accuracy=.740,F1=.734,Precision=.737,Recall=.740,MCC=.447),dict(model='Random Forest',AUC=.871,Accuracy=.795,F1=.793,Precision=.793,Recall=.795,MCC=.568),dict(model='Tree',AUC=.767,Accuracy=.749,F1=.748,Precision=.748,Recall=.749,MCC=.475)]
    write_csv(out/'model_comparison.csv',scores)
    summary=dict(reservations=len(clean),capacity=CAPACITY,mean_cancellation_probability=sum(i['CancellationProbability'] for i in clean)/len(clean),expected_non_cancelled_reservations=sum(1-i['CancellationProbability'] for i in clean),booked_room_nights=sum(i['bookings'] for i in dates),expected_room_nights=sum(i['expected'] for i in dates),peak_bookings=max(i['bookings'] for i in dates),peak_expected_room_use=max(i['expected'] for i in dates),over_capacity_dates=[i['date'] for i in dates if i['bookings']>CAPACITY],nightly=dates,model_comparison=scores)
    (out/'dashboard_data.json').write_text(json.dumps(summary,indent=2)+'\n')
    provenance=dict(source='User-executed Orange Random Forest predictions; no model rerun in dashboard code',evaluation='User screenshot, five-fold stratified cross-validation; scores rounded to three decimals',class_1='Canceled',class_0='Not canceled',source_row_order_verified=True,assumptions=['One room per reservation','All supplied stays counted from arrival inclusive to departure exclusive','No additional bookings or out-of-service rooms included','Probability estimates are uncalibrated and may not transfer from 2015–2016 training data to 2026 planned bookings'],sha256={f:hashlib.sha256((BASE/f).read_bytes()).hexdigest() for f in ['hotel_predictions.tab','planned_reservations.csv']})
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    html=(BASE/'dashboard_template.html').read_text()
    html=html.replace('/*DATA*/{}',json.dumps(summary).replace('<','\\u003c'))
    (BASE/'dashboard.html').write_text(html)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['nightly','model_comparison']},indent=2))


if __name__=='__main__':
    main()
