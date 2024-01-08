import cv2
from pathlib import Path
import glob
import pandas as pd
import pathlib


def getData(path):
    h = []
    s = []
    v = []
    hasil = []
    filename = []

    path = glob.glob(path)

    for i, item in enumerate(path):
        img = cv2.imread(item, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        num_rows, num_cols = img.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((num_cols / 2, num_rows / 2), 0, 1)
        img = cv2.warpAffine(img, rotation_matrix, (num_cols, num_rows))

        imS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        paa = 960
        paz = paa + 260
        laa = 960
        laz = laa + 220
        ROI = imS[paa:paz, laa:laz]
        
        ROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2RGB)

        hsv = cv2.cvtColor(ROI, cv2.COLOR_BGR2HSV)
        inputhsv = cv2.mean(hsv)

        h.append(inputhsv[0])
        s.append(inputhsv[1])
        v.append(inputhsv[2])
        hasil.append(0)
        filename.append(Path(item).stem)

    return h, s, v, hasil, filename

def getDataFrame(path):
    h, s, v, hasil, filename = getData(path)

    header = ['h', 's', 'v', 'hasil', 'filename']
    df = pd.DataFrame(list(zip(h, s, v, hasil, filename)), columns=header)
    path = pathlib.PurePath(path)
    df = df.assign(hasil=path.parent.name)

    return df

if __name__ == '__main__':
    print(getData(r'dataset/unriped/*.jpeg'))
    print(getDataFrame(r'dataset/unriped/*.jpeg'))
