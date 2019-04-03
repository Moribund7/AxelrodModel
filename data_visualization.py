import json
import matplotlib.pyplot as plt
import glob


def create_dict_of_variables(data):
    dict_of_variables = {}
    for q in data:
        dict_of_variables["q"] = []
        for key in data[q].keys():
            key_str = str(key)
            dict_of_variables[key_str] = []
    return dict_of_variables


def add_data_to_dict_of_variables(data, dict_of_variables):
    for q in data:
        dict_of_variables["q"].append(q)
        for element in data[q]:
            dict_of_variables[element].append(data[q][element])

def load_all_json_data():
    dict_of_variables = None
    for filename in glob.glob('*.json'):
        with open(filename, "r") as f:
            data = json.load(f)
        if dict_of_variables == None:
            dict_of_variables = create_dict_of_variables(data)
        add_data_to_dict_of_variables(data, dict_of_variables)
    return dict_of_variables
if __name__ == "__main__":



    dict_of_variables = load_all_json_data()


    plt.figure()

    for element in dict_of_variables:
        if element != "q":
            plt.plot(dict_of_variables["q"], dict_of_variables[element], 'o', label=element)  # TODO refactor

    plt.legend()
    plt.xscale('log')
    plt.show()
