
with open('/home/arya/my_python/my_torch/cq/noun_data/clean_train.code','r') as f:
    codelines=f.readlines()[:5]
with open('/home/arya/my_python/my_torch/cq/noun_data/clean_train.comment','r') as f:
    commentlines=f.readlines()[:5]

for i in range(len(codelines)):
    codelines[i]=codelines[i].strip()
    commentlines[i]=commentlines[i].strip()
    





