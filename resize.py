import cv2
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from sklearn import linear_model


def main():
    data_dir_path = u"./data_hm_pred_new"
    file_list = os.listdir(r'./data_hm_pred_new')

    x = np.empty(0, np.int)
    y = np.empty(0, np.int)


    im = 0
    jm = 0
    for file_name in file_list:
        root, ext = os.path.splitext(file_name)
        
        b = 0
        
        if ext == u'.jpg':
            abs_name = data_dir_path + '/' + file_name
            img = cv2.imread(abs_name)
            print("Load {}".format(file_name))
            #print(img.shape)

            #img = img[0 : 200, 0 : 100]
            #cv2.imwrite(abs_name, img)
            

    """
            black = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            for i in range(black.shape[0]):
                for j in range(black.shape[1]):
                    if black[i][j] == 0:
                        black[i][j] = 255
                        b = b + 1
                        if im < i:
                            im = i
                        if jm < j:
                            jm = j
                    elif black[i][j] == 127:
                        black[i][j] = 0
                    else:
                        black[i][j] = 0

    print(im, jm)
    """

    return 0


if __name__ == '__main__':
    main()
