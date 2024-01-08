import DatabaseCreator as dcr
import DistanceComparator as dco

class TomatoClassifier:

    def create_base(self):
        self.base_creator = dcr.DatabaseCreator()
        self.base_creator.createDB_All()

    def classify_tomato(self, path_test, metric):
        self.distance_calculator = dco.DistanceComparator()
        matang, mentah = self.distance_calculator.distanceComparison(path_test, metric)
        result = "Matang" if matang > mentah else "Mentah"
        return result

if __name__ == '__main__':
    classifier = TomatoClassifier()
    classifier.create_base()
    path_test = 'dataset/test/*'
    metric = 'canberra'
    hasil_prediksi = classifier.classify_tomato(path_test, metric)
    print("\nHasil Prediksi adalah", hasil_prediksi)
