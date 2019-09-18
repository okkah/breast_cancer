import numpy as np
import sys
import os
import cv2
import argparse
import multiresolutionimageinterface as mir


def main():
    parser = argparse.ArgumentParser(description="CAMELYON17 dataset Preprocess")
    parser.add_argument('--tif', '-t', default="center_0/patient_013/patient_013_node_3.tif",
                        help='tif file path')
    parser.add_argument('--annotations', '-a', default="patient_013_node_3",
                        help='annotations file path')
    parser.add_argument('--level', '-l', type=int, default=2,
                        help='down-sampling level')
    parser.add_argument('--resize', '-r', type=int, default=32,
                        help='resize times')
    parser.add_argument('--patch', '-p', type=int, default=256,
                        help='patch size')
    parser.add_argument('--out', '-o', default="other/",
                        help='output directory path')
    args = parser.parse_args()

    # Load TIFF
    reader = mir.MultiResolutionImageReader()
    tif_dir = "../../../mnt/nas/CAMELYON/CAMELYON17/original/org/training/"
    tif_path = tif_dir + args.tif
    mr_image = reader.open(tif_path)
    w_max, h_max = mr_image.getDimensions()
    print("Load {}".format(args.tif) + " (" + str(w_max) + "×" + str(h_max) + " pixels)")
    #print(mr_image)

    # Annotations
    annotation_list = mir.AnnotationList()
    xml_repository = mir.XmlRepository(annotation_list)
    xml_dir = "../../../mnt/nas/CAMELYON/CAMELYON17/original/org/training/lesion_annotations/"
    xml_path = xml_dir + args.annotations + '.xml'
    xml_repository.setSource(xml_path)
    xml_repository.load()
    annotation_mask = mir.AnnotationToMask()

    camelyon17_type_mask = True
    label_map = {'metastases': 1, 'normal': 2} if camelyon17_type_mask else {'_0': 1, '_1': 1, '_2': 0}
    conversion_order = ['metastases', 'normal'] if camelyon17_type_mask else  ['_0', '_1', '_2']

    """
    annotation_mask.convert(annotation_list, "annotations/" + args.annotations + '.tif',
                            mr_image.getDimensions(), mr_image.getSpacing(),
                            label_map, conversion_order)
    print("Got annotation")
    sys.exit()
    """

    # Extract patch
    mr_imagea = reader.open("annotations/" + args.annotations + ".tif")
    ds = mr_image.getLevelDownsample(args.level)
    w_lmax, h_lmax = int(w_max/ds), int(h_max/ds)
    
    """
    imagea = mr_imagea.getUCharPatch(int(0 * ds), int(0 * ds), w_lmax, h_lmax, args.level)
    #print(imagea.shape)
    imga = cv2.resize(imagea, (int(w_lmax * 1/args.resize), int(h_lmax * 1/args.resize)))
    #print(imga.shape)

    c = 0
    for i in range(imga.shape[0]):
        for j in range(imga.shape[1]):
            if imga[i][j] != 0:
                c = c + 1
            else:
                imga[i][j] = 255
            print(c)

    cv2.imwrite(args.out + "c.jpg", imga)
    """

    image = mr_image.getUCharPatch(int(0 * ds), int(0 * ds), w_lmax, h_lmax, args.level)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    img = cv2.resize(image, (int(w_lmax * 1/args.resize), int(h_lmax * 1/args.resize)))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    c = 0
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            c = c + 1
            print(str(c) + "/" + str(gray.shape[0] * gray.shape[1]))
            if gray[i][j] < 5:
                gray[i][j] = 255
    ret, thresh = cv2.threshold(gray, 204, 255, cv2.THRESH_BINARY)
    cv2.imwrite(args.out + "a.jpg", img)
    #cv2.imwrite(args.out + "b.jpg", thresh)
    sys.exit()

    c = 0
    d = 0
    e = 0
    f = 0
    for row in range(0, int(h_lmax/args.resize - args.patch/args.resize),
                     int(args.patch/args.resize)):
        for col in range(0, int(w_lmax/args.resize - args.patch/args.resize),
                         int(args.patch/args.resize)):
            thresh_patch = thresh[row : row + int(args.patch/args.resize),
                            col : col + int(args.patch/args.resize)]
            #print(thresh_patch.shape)
            #print(row, col)
            c = c + 1

            flag = False
            for i in range(int(args.patch/args.resize)):
                for j in range(int(args.patch/args.resize)):
                    if thresh_patch[i][j] == 0:
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

                        #if tumor/(args.patch/args.resize) >= 0.75:
                        if tumor/(args.patch/args.resize) != 0:
                            #cv2.imwrite(args.out + "positive/" + args.annotations
                            #            + "_" + str(row2) + "_" + str(col2) + ".jpg", image_patch)
                            e = e + 1
                        #elif tumor/(args.patch/args.resize) != 0:
                            #cv2.imwrite(args.out + "positive2/" + args.annotations
                                        #+ "_" + str(row2) + "_" + str(col2) + ".jpg", image_patch)
                            #f = f + 1
                        else:
                            #cv2.imwrite(args.out + "negative/" + args.annotations
                            #            + "_" + str(row2) + "_" + str(col2) + ".jpg", image_patch)
                            d = d + 1

                        break
                if flag:
                    break

    #print(str(e) + "/" + str(f) +  "/" + str(d) + "/" + str(c))
    print(str(e) + "/" + str(d) + "/" + str(c))

    return 0


if __name__ == '__main__':
    main()
