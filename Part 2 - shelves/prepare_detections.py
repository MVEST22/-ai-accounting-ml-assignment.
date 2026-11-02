import json
from pathlib import Path
# Materialize the LLM's structured visual response and user-supplied model outputs.
# This is a replay/capture script, not an inference API client.
base=Path(__file__).resolve().parent
(base/'results').mkdir(exist_ok=True)
raw={
'0009':[(561.5,585.5,19,51,.262,'e9054a54-a66b-4f43-8cf6-78743fc04482')],
'0010':[(150,410.5,132,37,.366,'883476bd-744b-4acb-856e-c655e90e2a7b')],
'0011':[(324,257.5,20,37,.254,'9f872db6-87f1-451b-8435-42f1ff452ac8')],
'0012':[
(56.5,59.5,25,33,.717,'090218dd-d686-41ff-ab5a-16e12efacb23'),
(303.5,124,17,60,.679,'6db20458-9465-42e9-97f8-800a656d6c05'),
(142,356,34,56,.657,'dd7c3144-368e-458e-bedb-03a6f7d75aa8'),
(552,275.5,20,15,.546,'ea44fc57-321b-42c3-89d6-68bc2ca70f49'),
(429.5,530,13,36,.454,'ebf4a899-5ce4-4f27-9598-a7511ffdf658'),
(238.5,572,33,58,.447,'fa2e08c9-db71-414d-a1d7-4004d9fceb8a'),
(478.5,84.5,25,55,.436,'7dd1de92-2231-41e3-8c51-87fbb522bbe3'),
(301,253.5,82,13,.323,'e13958f4-30e9-4879-b8d4-0d7104996ca7'),
(157,69,66,30,.319,'fdc89b58-3ac2-4b0a-8ea6-5b8ced497288'),
(369.5,262,33,24,.278,'2486597f-cb78-4367-84e0-79703d4c000e')],
'0014':[
(305,554,32,42,.811,'22b9d528-362b-49d9-88c6-c3c94fc882de'),
(286,207,80,44,.801,'618d9251-4bdf-4133-aa57-c68e2b7b997c'),
(241,618,36,40,.76,'e2fa4680-b9dd-407a-b997-1b28eade40a4'),
(468.5,216,19,42,.747,'dd703fbb-ec8b-46bd-9367-29626a7ff806'),
(222,136,26,50,.676,'e7875986-a2a9-49e0-9653-7220c37b3070'),
(463,338,18,36,.645,'0db17d54-5262-4a3b-9573-61d12b51eefd'),
(195.5,563.5,15,33,.575,'fd0f0021-8ee2-4095-b02d-3e0eae154ab6'),
(631,264,18,48,.551,'64c83531-c2f5-47f0-bfb2-a8196eb586a8'),
(390.5,454,21,40,.545,'b4f7293a-6b92-4711-9e9d-5acd870d16da'),
(172.5,326,17,32,.506,'2569a5bb-01a8-4204-96c7-3e4ed23bf789'),
(127.5,195,33,46,.458,'a38ed29e-6347-4370-9b35-25bafd3ae377'),
(573,325.5,64,19,.398,'2e774c80-6577-4dc4-a8d9-3d2963a26e52'),
(549.5,576,49,28,.391,'b3d62a1d-6829-4e16-a3a1-3ec665401a98'),
(586,163.5,68,33,.344,'75921769-8c46-45fd-827b-3c494d2ccbbf'),
(413.5,394.5,37,39,.314,'56423c84-3490-41b0-8939-fc8bd726da92'),
(579,244.5,66,17,.283,'faeb0910-7536-451c-853d-fa6e63c50aeb'),
(372,510,14,28,.274,'0f538b09-8a81-4f07-91ab-62e86d62484b')],
'0017':[
(303,441.5,54,49,.826,'94856e13-9842-48b7-ac57-31005f6918a1'),
(317,507.5,74,43,.812,'f1083a02-857b-49ae-b208-ddb49a6657e4'),
(242,228.5,56,61,.765,'87f4bdd4-b9a1-48cc-ae3b-a0c65a4fd2ae'),
(231,576.5,88,47,.759,'65a02c46-1eba-4cd8-b0d4-b2a1eba8a916'),
(241.5,75,25,46,.715,'568212c9-f190-4f8c-ad3d-8d1cfb794c65'),
(236,148.5,14,43,.702,'56b36fd3-d426-4b9c-af29-e314f4dc38d8'),
(547.5,488,27,32,.614,'28868399-ca10-48fd-b1aa-e22d76624fb8'),
(546.5,543.5,33,39,.461,'e3904559-c5c6-4e67-a031-0cfb970ecaee'),
(67,216,12,54,.457,'f911d9d2-0558-4395-a453-14ab7ec9614d'),
(577,258.5,10,31,.305,'efdf6613-2ea5-4589-9ca7-45b2fa70c601'),
(101.5,58,11,48,.279,'ecafe3fc-cad8-4246-b2d1-56e8e5566258')],
'0019':[
(100.5,595,37,52,.702,'39e413dd-b275-4512-8155-ca4d9879e677'),
(217.5,511,27,40,.69,'b60f20c8-33e1-4f4a-a5d9-0d709b0459fb'),
(293.5,45.5,61,41,.608,'7adfe9fa-3890-4323-acd7-beeebd80e6d7'),
(574,252,32,22,.529,'ff24ff34-4e17-4096-b7af-92960053688d'),
(633.5,343.5,13,21,.475,'dad16ecc-8546-484b-b144-d7b394e6bf34'),
(147,311.5,16,49,.276,'f6c3f1ae-21a0-423f-9143-b053017f2b6a')]
}
llm={
'0009':[(346,356,43,106,'Gap between milk cartons on the third visible shelf')],
'0010':[(75,392,143,40,'Broad empty front section on the second shelf from the bottom')],
'0011':[(250,166,56,54,'Gap between yellow packets and purple tubs')],
'0012':[(45,42,27,42,'Upper left gap'),(124,48,63,34,'Gap above small packets'),(292,95,22,59,'Tall gap between packet groups'),(462,57,32,57,'Upper right gap'),(119,326,42,63,'Gap between yellow and red cartons'),(187,547,67,62,'Lower shelf gap'),(420,512,27,47,'Lower shelf gap beside cartons')],
'0014':[(210,111,26,48,'Upper shelf gap'),(111,172,33,48,'Left gap on third shelf'),(244,181,84,49,'Large central gap'),(459,195,20,45,'Gap before red jars'),(626,241,14,47,'Gap at right edge'),(165,307,19,36,'Gap between jars'),(454,319,18,36,'Gap before red jars'),(394,375,39,38,'Recessed stock and exposed front shelf'),(381,433,20,40,'Gap beside bottles'),(187,547,17,33,'Small lower shelf gap'),(287,532,35,47,'Central lower shelf gap'),(224,597,37,41,'Bottom shelf gap')],
'0017':[(231,52,25,48,'Upper left gap'),(225,126,18,44,'Gap beside white labels'),(211,197,61,63,'Wide middle left gap'),(275,416,57,57,'Gap beside small bottles'),(279,482,77,49,'Wide lower middle gap'),(185,550,89,52,'Bottom left gap'),(532,472,28,34,'Lower right gap'),(530,524,34,39,'Bottom right gap')],
'0019':[(264,24,61,39,'Top shelf central gap'),(136,287,22,48,'Gap beside dark bottles'),(204,489,30,44,'Lower central gap'),(82,570,37,52,'Bottom left gap'),(559,240,34,30,'Right shelf gap')]
}
model={'source':'User-copied Roboflow Universe Try This Model JSON, supplied in conversation; not an API run by this script','model_id':'empty-shelf-detection-r8cfz/1','model_url':'https://universe.roboflow.com/twar/empty-shelf-detection-r8cfz','confidence_threshold':.25,'overlap_threshold':.5,'images':[]}
response={'source':'Interactive ChatGPT visual assessment of original 640x640 photos; approximate boxes, not ground truth. Produced after Roboflow outputs were visible, so this is not a blinded evaluation.','unit':'contiguous visible empty front-facing shelf area, not missing product units','images':[]}
for p in sorted(base.glob('zone*/*.jpg')):
 k=p.name.split('WA')[1][:4];path=p.relative_to(base).as_posix()
 preds=[dict(x=x,y=y,width=w,height=h,confidence=c,**{'class':'Empty-space'},class_id=0,detection_id=i) for x,y,w,h,c,i in raw[k]]
 model['images'].append({'image':path,'width':640,'height':640,'predictions':preds})
 boxes=[{'x1':x,'y1':y,'x2':x+w,'y2':y+h,'reason':r} for x,y,w,h,r in llm[k]]
 response['images'].append({'image':path,'width':640,'height':640,'boxes':boxes})
for name,data in [('roboflow_browser.json',model),('llm_response.json',response)]:
 (base/'results'/name).write_text(json.dumps(data,indent=2)+'\n')
print('Roboflow counts:',[len(i['predictions']) for i in model['images']])
print('LLM counts:',[len(i['boxes']) for i in response['images']])
