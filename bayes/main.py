import pandas as pd
import numpy as np


def read_file(filename):
    data = pd.read_csv(filename, ';')
    return data


def rand_symp(symp):
    patient = np.random.randint(0, 2, 23)
    symptoms = []
    for idx, disease in enumerate(symp['symptom']):
        if patient[idx] == 1:
            symptoms.append(disease)

    return symptoms


def dis_prob(symptoms, symptoms_probs, diseases):
    probs = {}
    for column in symptoms_probs.columns[1:]:
        prob = 1
        for symptom in symptoms:
            value = symptoms_probs[symptoms_probs.symptom == symptom][column].values[0]
            prob *= value
        probs[str(column)] = prob
    i = 0
    for prob in probs.keys():
        if (diseases["disease"].loc[i] == prob):
            probs[prob] *= diseases['prob'].loc[i]
        i = i + 1

    return probs



if __name__ == '__main__':
    symptoms = read_file('symptom.csv')
    diseases = read_file('disease.csv')
    diseases['prob'] = diseases['patient count']/list(diseases['patient count'])[-1]
    sympt_number = symptoms.shape[0]
    personal = rand_symp(symptoms)
    print("Symptoms: ", personal)
    probs = dis_prob(personal, symptoms, diseases)
    max = max(probs.values())
    for k, v in probs.items():
        if v == max:
            print("Disease ", k)
            break

