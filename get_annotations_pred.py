import cv2
import numpy as np
import sys
import os
import re
import pickle


def main():
    data_dir_path = u"./dataset2/test"
    file_list = os.listdir(r'./dataset2/test')

    width = 1000
    height = 1000

    image = np.ones((height, width), np.uint8) * 255

    with open('img_path.pkl', 'rb') as rf:
        img_path = pickle.load(rf)
    with open('img_pred.pkl', 'rb') as rf:
        img_pred = pickle.load(rf)
 
    print(image.shape, len(img_path), len(img_pred))

    for i in range(len(img_path)):
        m = re.findall(r'\d+', img_path[i])
        m1 = int(int(m[1]))
        m2 = int(int(m[2]))
        mh = int(int(m[3])/256)
        mw = int(int(m[4])/256)

        if img_pred[i] == 1:
            image[mh][mw] = 0
        elif img_pred[i] == 2:
            image[mh][mw] = 127
            
    cv2.imwrite("./data_hm_pred_new/" + str(m1) + "_" + str(m2) + ".jpg", image)

    return 0


if __name__ == '__main__':
    main()
