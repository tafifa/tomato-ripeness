import pandas as pd
import numpy as np
from sklearn import neighbors
import glob
import os
import DataProcessor as dp

class DistanceComparator:

    def __init__(self):
        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'csv/basis_pengetahuan.csv'))
        self.data = pd.read_csv(self.file_path)
        self.x = np.array(self.data[['h', 's', 'v']])
        self.y = np.array(self.data[['hasil']]).ravel()

    def distanceComparison(self, path, metric):
        self.knn = neighbors.KNeighborsClassifier(metric=metric, n_neighbors=1)
        self.knn.fit(self.x, self.y)
        valMatang, valMentah = 0, 0

        file_paths = glob.glob(path)

        if not file_paths:
            print('No image files found in the specified directory:', path)
        else:
            for item in file_paths:
                h, s, v, hasil, filename = dp.getData(item)
                inputTest = np.array([h, s, v]).reshape(1, -1)
                result = self.knn.predict(inputTest).reshape(1, -1)

                if result[0] == "riped":
                    valMatang += 1
                else:
                    valMentah += 1

        return valMatang, valMentah

if __name__ == '__main__':
    comparator = DistanceComparator()
    print(comparator.distanceComparison(r'dataset/test/*', 'canberra'))
