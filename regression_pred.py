import cv2
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from sklearn import linear_model


def get_maximum_area(img_src):
    label = cv2.connectedComponentsWithStats(img_src)

    n = label[0] - 1
    data = np.delete(label[2], 0, 0)
    maximum_area_id = 0
    maximum_area = data[0][4]

    for i in range(n):
        if data[i][4] > maximum_area:
            maximum_area_id = i
            maximum_area = data[i][4]

    return maximum_area


def get_data(black, gray, x, y, b, g):
    if b != 0:
        x = np.append(x, get_maximum_area(black))
        x0 = get_maximum_area(black)
    else:
        x = np.append(x, 0)
        x0 = 0

    if g != 0:
        y = np.append(y, get_maximum_area(gray))
        y0 = get_maximum_area(gray)
    else:
        y = np.append(y, 0)
        y0 = 0

    print("black=" + str(x0) + ", gray=" + str(y0))

    return x, y



def main():
    data_dir_path = u"./data_hm_pred"
    file_list = os.listdir(r'./data_hm_pred')

    x = np.empty(0, np.int)
    y = np.empty(0, np.int)

    for file_name in file_list:
        root, ext = os.path.splitext(file_name)
        
        b = 0
        g = 0
        
        if ext == u'.jpg':
            abs_name = data_dir_path + '/' + file_name
            img = cv2.imread(abs_name)
            print("Load {}".format(file_name))
            #print(img.shape)

            black = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            for i in range(black.shape[0]):
                for j in range(black.shape[1]):
                    if black[i][j] == 0:
                        black[i][j] = 255
                        b = b + 1
                    elif black[i][j] == 127:
                        black[i][j] = 0
                    else:
                        black[i][j] = 0
           
            for i in range(gray.shape[0]):
                for j in range(gray.shape[1]):
                    if gray[i][j] == 0:
                        gray[i][j] = 0
                    elif gray[i][j] == 127:
                        gray[i][j] = 255
                        g = g + 1
                    else:
                        gray[i][j] = 0

            x, y = get_data(black, gray, x, y, b, g)
    
            if b >= 200:
                print("macro")
            elif b >= 3 or g >= 5:
                print("micro")
            elif b == 0 and g == 0:
                print("negative")
            else:
                print("itc")
            
    #print(x, y)

    """
    plt.title('CAMELYON17 dataset heatmap regression')
    plt.scatter(x, y, s=20, c='blue', alpha=0.5)
    plt.xlabel('75% or more tumor (black)')
    plt.ylabel('less than 75% tumor (gray)')
    #plt.xlim(-2, 12)
    #plt.xlim(-50, 350)
    plt.show()
    """

    return 0


if __name__ == '__main__':
    main()
