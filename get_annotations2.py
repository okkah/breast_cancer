import cv2
import numpy as np
import sys
import os
import xml.etree.ElementTree as ET 


def main():
    data_dir_path = u"../../../mnt/nas/CAMELYON/CAMELYON17/original/org/training/lesion_annotations/"
    file_list = os.listdir(r'../../../mnt/nas/CAMELYON/CAMELYON17/original/org/training/lesion_annotations/')

    width = 159568
    height = 183378

    #image_w = np.ones((height, width), np.uint8) * 255
    #print("Got white image")
 
    for file_name in file_list:
        root, ext = os.path.splitext(file_name)
        #image = np.copy(image_w)
        image = np.ones((height, width), np.uint8) * 255
        
        if ext == u'.xml':
            abs_name = data_dir_path + '/' + file_name
            #abs_name = data_dir_path + '/' + "patient_012_node_0.xml"
            tree = ET.parse(abs_name) 
            root = tree.getroot()
            print("Load {}".format(file_name))

            for i in range(len(root[0])):
                w_min = 159568
                w_max = 0
                h_min = 183378
                h_max = 0

                for j in root[0][i][0]:
                    if w_min > int(float(j.get('X'))):
                        w_min = int(float(j.get('X')))
                    if w_max < int(float(j.get('X'))):
                        w_max = int(float(j.get('X')))
                    if h_min > int(float(j.get('Y'))):
                        h_min = int(float(j.get('Y')))
                    if h_max < int(float(j.get('Y'))):
                        h_max = int(float(j.get('Y')))

                w_img = w_max - w_min
                h_img = h_max - h_min
                #print(w_min, w_max, h_min, h_max)
                #print(w_img, h_img)

                d = 0
                points = np.empty((0, 2), int)
                img = np.ones((h_img, w_img), dtype=np.uint8) * 255
                for j in root[0][i][0]:
                    #img[int(float(j.get('Y'))) - h_min - 1][int(float(j.get('X'))) - w_min - 1] = 0
                    points = np.append(points, np.array([[int(float(j.get('X'))) - w_min, int(float(j.get('Y'))) - h_min]]), axis=0)
                    d = d + 1

                #print(str(d) + '/' + str(img.shape[0] * img.shape[1]))
                points = points.reshape(1, -1, 2)
                #print(points.shape)
                img = cv2.fillPoly(img, points, color=0) 
                #print(img)
                #print(image.shape)
                #print(img.shape)

                #print(h_min, h_min + img.shape[0], w_min, w_min + img.shape[1])
                image[h_min : h_min + img.shape[0], w_min : w_min + img.shape[1]] = img
                #cv2.imwrite("./other/" + str(i) + ".jpg", img)

            image = cv2.resize(image, (int(width * 1/32), int(height * 1/32)))
 
            """
            tmp = image[:, :]
            h, w = image.shape[:2]
            if(h > w):
                size = h
                limit = w
            else:
                size = w
                limit = h
            start = int((size - limit) / 2)
            fin = int((size + limit) / 2)
            image = cv2.resize(np.ones((1, 1), np.uint8) * 255, (size, size))
            if(size == h):
                image[:, start:fin] = tmp
            else:
                image[start:fin, :] = tmp

            image = cv2.resize(image, dsize=(256, 256))
            """
            
            image_new = np.ones((int(image.shape[0]/8), int(image.shape[1]/8)), dtype=np.uint8) * 255
 
            for row in range(0, image.shape[0]-8, 8):
                for col in range(0, image.shape[1]-8, 8):
                    image_patch = image[row : row+8, col : col+8]
                    #print(image_patch.shape)
                    #print(row, col)

                    tumor = 0
                    for i in range(8):
                        for j in range(8):
                            if image_patch[i][j] == 0:
                                tumor = tumor + 1
 
                    #print(tumor)

                    if tumor/64 >= 0.75:
                        image_new[int(row/8)][int(col/8)] = 0
                    elif tumor != 0:
                        image_new[int(row/8)][int(col/8)] = 127
            
            cv2.imwrite("./data_hm/" + file_name + ".jpg", image_new)
            #cv2.imwrite("./data_hm/" + "patient_012_node_0.xml" + ".jpg", image_new)

    """
    c = 0
    d = 0
    e = 0
    for row in range(0, image.shape[0] - 256), 256):
        for col in range(0, image.shape[1] - 256), 256):
            image_patch = image[row : row + 256, col : col + 256]
            #print(image_patch.shape)
            #print(row, col)
            c = c + 1

            flag = False
            for i in range(256):
                for j in range(256):
                    if image_patch[i][j] == 0:
                        flag = True

                        row2 = row * args.resize
                        col2 = col * args.resize
                        image_patch = image[row2 : row2 + args.patch,
                                            col2 : col2 + args.patch]
                        #print(image_patch.shape)

                        tumor = 0
                        for i2 in range(int(args.patch/args.resize)):
                            for j2 in range(int(args.patch/args.resize)):
                                #print(row + i2, j + j2)
                                if imga[row + i2][col + j2] != 0:
                                    tumor = tumor + 1
                        print(tumor)

                        if tumor/(args.patch/args.resize) >= 0.75:
                            #cv2.imwrite(args.out + "positive/" + args.annotations
                            #            + "_" + str(row2) + "_" + str(col2) + ".jpg", image_patch)
                            e = e + 1
                        else:
                            #cv2.imwrite(args.out + "negative/" + args.annotations
                            #            + "_" + str(row2) + "_" + str(col2) + ".jpg", image_patch)
                            d = d + 1

                        break
                if flag:
                    break

    print(str(e) + "/" + str(d) + "/" + str(c))
    """


    """
            image[int(float(j.get('Y')))][int(float(j.get('X')))] = 0
            print(int(float(j.get('X'))), int(float(j.get('Y'))))

    image = cv2.resize(image, (int(width * 1/32), int(height * 1/32)))
    print(image.shape)

    d = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i][j] == 0:
                d = d + 1
    print(d)
    """

    #cv2.imwrite("./other/a.jpg", image)

 
    """
    for file_name in file_list:
        root, ext = os.path.splitext(file_name)
        
        if ext == u'.png' or u'.jpeg' or u'.jpg':
            # 画像の読み込み
            abs_name = data_dir_path + '/' + file_name
            img = cv2.imread(abs_name) 
            print("Load {}".format(abs_name))

            # ラベリング結果書き出し用に二値画像をカラー変換
            color_src = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

            # 画像の保存
            cv2.imwrite(abs_name, img3)
    """

    return 0


if __name__ == '__main__':
    main()
