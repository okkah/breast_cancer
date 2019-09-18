import cv2
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from sklearn import linear_model

DATA_DIR = os.path.join('dataset_hm2')


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
    dirs = os.listdir(DATA_DIR)

    x_macro = np.empty(0, np.int)
    y_macro = np.empty(0, np.int)
    x_micro = np.empty(0, np.int)
    y_micro = np.empty(0, np.int)
    x_itc = np.empty(0, np.int)
    y_itc = np.empty(0, np.int)
    x_negative = np.empty(0, np.int)
    y_negative = np.empty(0, np.int)
 
    target_dirs = []
    for dir in dirs:
        if os.path.isdir(os.path.join(DATA_DIR, dir)):
            target_dirs.append(dir)

    dirs = [dir for dir in target_dirs]

    target_all_files = []
    for dir in dirs:
        target_dir = os.path.join(DATA_DIR, dir)
        print('\n' + target_dir)

        files = os.listdir(target_dir)

        target_files = []
        for file in files:
            b = 0
            g = 0
            
            if file.endswith('.jpg'):
                img = cv2.imread(os.path.join(target_dir, file))
                print("Load {}".format(file))
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

                if dir == 'macro':
                    x_macro, y_macro = get_data(black, gray, x_macro, y_macro, b, g)
                elif dir == 'micro':
                    x_micro, y_micro = get_data(black, gray, x_micro, y_micro, b, g)
                elif dir == 'itc':
                    x_itc, y_itc = get_data(black, gray, x_itc, y_itc, b, g)
                elif dir == 'negative':
                    x_negative, y_negative = get_data(black, gray, x_negative, y_negative, b, g)
                
                #print(x, y)

    plt.title('CAMELYON17 dataset heatmap regression')
    plt.scatter(x_macro, y_macro, s=20, c='red', alpha=0.5, label='macro')
    plt.scatter(x_micro, y_micro, s=20, c='blue', alpha=0.5, label='micro')
    plt.scatter(x_itc, y_itc, s=20, c='green', alpha=0.5, label='itc')
    plt.scatter(x_negative, y_negative, s=20, c='gray', alpha=0.5, label='negative')
    plt.xlabel('75% or more tumor (black)')
    plt.ylabel('less than 75% tumor (gray)')
    #plt.xlim(-2, 12)
    #plt.xlim(-50, 350)
    plt.legend()
    plt.show()

    return 0


if __name__ == '__main__':
    main()
