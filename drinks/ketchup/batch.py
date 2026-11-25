# python3 batch.py 13 24 -> JSON requests for generate_image_batch
import sys,json; from shots import prompt
a,b=int(sys.argv[1]),int(sys.argv[2])
print(json.dumps([{"index":i,"params":{"model":"gpt_image_2_6","aspect_ratio":"16:9","use_unlim":False,"prompt":prompt(i)}} for i in list(range(a,b+1))+[int(x) for x in sys.argv[3:]]]))
