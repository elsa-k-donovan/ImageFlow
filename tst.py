import json
from jsonmerge import merge,Merger

x = []
x = json.dumps(x)

# for i in range(5):
#     z = json.loads(x)
#     dic = json.dumps([{
#         'A':i,
#         'B':i,
#         'C':i,
#         }])
#     z.update(dic)
#     x = json.dumps([z])

# print(x)

print("here")
schema = {'data' : {
          'mergeStrategy': 'append',
          'mergeOptions': {'ignoreDups': True}}}
merger = Merger(schema)
head = {"data" : []}
dic = {'data' :  {'A': 1, 'B': 2, 'C': 3, }}
dic2 = {'data' :{'A': 4, 'B': 5, 'C': 6, }}
z = merger.merge(head, [dic2])
print(z)
z = merger.merge(z , [dic])
print(z)
# # JSON data:
# x =         {
#     }
# x = json.dumps(x)
# print(x)
# # python object to be appended
# y = {"pin":110096}
# print(y)
# # parsing JSON string:
# z = json.loads(x)

# # appending the data
# z.update(y)
# print(z)
# # the result is a JSON string:
# print(json.dumps(z))
