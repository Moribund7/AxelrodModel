import json
import matplotlib.pyplot as plt

with open("data.json", "r") as f:
    data = json.load(f)

plt.figure()
for q in data:
    for element in data[q]:
        plt.scatter(q,data[q][element]) # TODO refactor, dodac poprawnie kolory

plt.show()
