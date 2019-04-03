import json
import matplotlib.pyplot as plt

with open("data.json", "r") as f:
    data = json.load(f)

plt.figure()

dict_of_variables={}
for q in data:
    dict_of_variables["q"]=[]
    for key in data[q].keys():
        key_str=str(key)
        dict_of_variables[key_str]=[]

for q in data:
    dict_of_variables["q"].append(q)
    for element in data[q]:
        dict_of_variables[element].append(data[q][element])


for element in dict_of_variables:
    if element != "q":
        plt.plot(dict_of_variables["q"],dict_of_variables[element],'o',label=element) # TODO refactor

plt.legend()
plt.xscale('log')
plt.show()
