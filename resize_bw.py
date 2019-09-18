import cv2
import numpy as np
import sys
import os


def main():
    data_dir_path = u"./dataset2"
    file_list = os.listdir(r'./dataset2')

    width = 150
    height = 300

    for file_name in file_list:
        root, ext = os.path.splitext(file_name)

        if ext == u'.jpg':
            abs_name = data_dir_path + '/' + file_name
            image = np.ones((height, width), np.uint8) * 255
            img = cv2.imread(abs_name)
            print("Load {}".format(file_name))
            #print(img.shape)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (int(img.shape[1] * 1/8), int(img.shape[0] * 1/8)))
  
            image[0 : img.shape[0], 0 : img.shape[1]] = img

            cv2.imwrite("data_hm_pred_new_bw/" + file_name, image)

    return 0


if __name__ == '__main__':
    main()
