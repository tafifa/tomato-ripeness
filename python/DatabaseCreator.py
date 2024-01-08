import pandas as pd
import pathlib

import DataProcessor as dp

class DatabaseCreator:

    def createDB(self, path):
        h, s, v, hasil, filename = dp.getData(path)

        header = ['h', 's', 'v', 'hasil', 'filename']
        df = pd.DataFrame(list(zip(h, s, v, hasil, filename)), columns=header)
        path = pathlib.PurePath(path)
        df = df.assign(hasil=path.parent.name)

        df.to_csv(rf'csv/basis_pengetahuan_{path.parent.name}.csv')

    def createDB_All(self):
        df_mentah = dp.getDataFrame(r'dataset/unriped/*.jpeg')
        df_matang = dp.getDataFrame(r'dataset/riped/*.jpeg')
        df_concat = pd.concat([df_mentah, df_matang], ignore_index=True)
        # print(df_concat)
        df_concat.to_csv('csv/basis_pengetahuan.csv')

if __name__ == '__main__':
    db_creator = DatabaseCreator()
    db_creator.createDB_All()
