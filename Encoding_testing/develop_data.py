import json

import numpy
import numpy as np

import matplotlib.pyplot as plt


def develop_data():
    array = np.array(json.load(open('distances.json')))

    array = np.unique(array)



    average = np.average(array)
    median = numpy.median(array)
    perc1 = np.percentile(array, 1)
    perc25 = np.percentile(array, 25)
    perc75 = np.percentile(array, 75)

    plt.hist(array, bins='auto')
    plt.xlabel('Distance')
    plt.ylabel('Amount')
    plt.show()

    #plt.boxplot(array, vert=True, sym='')
    #plt.show()





develop_data()