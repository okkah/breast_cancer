import cv2
import numpy as np
import sys
import os

def main():
    data_dir_path = u"./data_hm_pred_new_bw"
    file_list = os.listdir(r'./data_hm_pred_new_bw')
   
    for file_name in file_list:
        root, ext = os.path.splitext(file_name)
        
        if ext == u'.jpg':
            # 画像の読み込み
            abs_name = data_dir_path + '/' + file_name
            img = cv2.imread(abs_name) 
            print("Load {}".format(abs_name))

            # グレースケール化
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 大津の二値化
            img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

            k = 3
            for i in range(0, img.shape[0]-k, k):
                for j in range(0, img.shape[1]-k, k):
                    tumor = 0

                    for i1 in range(k):
                        for j1 in range(k):
                            if img[i+i1][j+j1] == 0:
                                tumor = tumor + 1
                    if tumor !=0:
                        for i1 in range(k):
                            for j1 in range(k):
                                img[i+i1][j+j1] = 0

            # 白黒反転 
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if img[i][j] == 0:
                        img[i][j] = 255
                    else:
                        img[i][j] = 0

            # ラベリング処理
            label = cv2.connectedComponentsWithStats(img)

            # オブジェクト情報を項目別に抽出
            n = label[0] - 1
            data = np.delete(label[2], 0, 0)
            center = np.delete(label[3], 0, 0)

            #最大面積の取得
            maximum_area_id = 0
            maximum_area_id2 = 0
            maximum_area_id3 = 0
            maximum_area = data[0][4] 
            maximum_area2 = data[0][4] 
            maximum_area3 = data[0][4] 
            for i in range(n):
                if data[i][4] > maximum_area:
                    maximum_area_id = i
                    maximum_area = data[i][4] 
            for i in range(n):
                if data[i][4] == maximum_area:
                    pass
                elif data[i][4] > maximum_area2:
                    maximum_area_id2 = i
                    maximum_area2 = data[i][4] 
            for i in range(n):
                if data[i][4] == maximum_area or maximum_area2:
                    pass
                if data[i][4] > maximum_area3:
                    maximum_area_id3 = i
                    maximum_area3 = data[i][4] 

            # 最大面積以外のものを消去
            for i in range(n):
                x0 = data[i][0]
                y0 = data[i][1]
                x1 = data[i][0] + data[i][2]
                y1 = data[i][1] + data[i][3]
                if i == maximum_area_id or maximum_area_id2 or maximum_area_id3:
                    pass
                else:
                    cv2.rectangle(img, (x0, y0), (x1, y1), 0, -1)

            label, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            image = np.ones((300, 200), np.uint8) * 255 
            for i in range(0, len(contours)):
                if len(contours[i]) > 0:
                    if cv2.contourArea(contours[i]) < 500:
                        continue

                cv2.polylines(image, contours[i], True, 0, 2)

            cv2.imwrite('data_hm_pred_new_shape/' + file_name, image)

    return 0

if __name__ == '__main__':
    main()
