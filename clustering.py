from PIL import Image
import numpy as np
from sklearn.cluster import DBSCAN
import cv2
from collections import Counter
import csv
import os

def extractSlicesandClusters(final_names):
    DIR_PATH = './testPatient/'
    OUTPUT_PATH = './'
    for f in final_names:

        image = cv2.imread(DIR_PATH+'/'+f)
        f = f[:len(f)-4]
        gray_scale = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        thresh = cv2.threshold(gray_scale,0,255,cv2.THRESH_BINARY)[1]

        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contours = contours[0] if len(contours) == 2 else contours[1]
        x_list = list()
        y_list = list()
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if w==4 and h==5:
                x_list.append(x)
                y_list.append(y)

        x_coord = Counter(x_list)
        y_coord = Counter(y_list)
        final_x = [x for x in x_coord.keys() if x_coord[x] > 1]
        final_x.sort()
        final_y = [y for y in y_coord.keys() if y_coord[y] > 1]
        final_y.sort()
        final_width = final_x[1] - final_x[0]
        final_height = final_y[1] - final_y[0]
        start_y = final_y[0] - final_height
        final_y.append(start_y)
        final_y.sort()

        name_idx = 1
        clusterCount = list()
        outputList = list()
        for y in final_y:
            for x in final_x:
                new_image = image[y+5:y+final_height, x+4:x+final_width]
                new_grayscale = cv2.cvtColor(new_image,cv2.COLOR_BGR2GRAY)
                if cv2.countNonZero(new_grayscale) != 0 and name_idx < 34:
                    cv2.imwrite(OUTPUT_PATH+'Slices/'+f+'/'+str(name_idx)+".png", new_image)

                    hsv_image = cv2.cvtColor(new_image,cv2.COLOR_BGR2HSV)
                    lower_red = np.array([0,100,20])
                    upper_red = np.array([10,255,255])
                    lower_orange = np.array([10,100,20])
                    upper_orange = np.array([27,255,255])
                    lower_blue = np.array([105,100,20])
                    upper_blue = np.array([125,255,255])
                    mask_red = cv2.inRange(hsv_image,lower_red,upper_red)
                    mask_orange = cv2.inRange(hsv_image,lower_orange,upper_orange)
                    mask_blue = cv2.inRange(hsv_image,lower_blue,upper_blue)
                    final_mask = mask_blue | mask_orange | mask_red
                    target = cv2.bitwise_and(new_image,new_image, mask=final_mask)
                    target_grayscale = cv2.cvtColor(target,cv2.COLOR_BGR2GRAY)
                    if cv2.countNonZero(target_grayscale) != 0:
                        cv2.imwrite(OUTPUT_PATH+'Color/'+f+'/'+str(name_idx)+".png", target)
                        

                        image11 = Image.open(OUTPUT_PATH+'Color/'+f+'/'+str(name_idx)+".png")
                        os.remove(OUTPUT_PATH+'Color/'+f+'/'+str(name_idx)+".png")
                        s = image11.getdata()
                        new_image1 = list()
                        for i in s:
                            if i[0] == 0 and i[1] == 0 and i[2] == 0:
                                new_image1.append((0, 0, 0))
                            else:
                                new_image1.append((255, 255, 0))
                    
                        image_array = np.array(new_image1)
                        image11.putdata(new_image1)
                        image11.save(OUTPUT_PATH+'Clusters/'+f+'/'+str(name_idx)+".png")
                        localCount = 0

                        output = DBSCAN(eps=6, min_samples=14).fit(image_array)
                        c = Counter(output.labels_)
                        for i in c.values():
                            if i >= 135:
                                localCount += 1
                        localList = [name_idx, localCount-1]
                        outputList.append(localList)
                        with open(OUTPUT_PATH+'Clusters/'+f+'/ClusterReport.csv', 'w') as file1:
                            heading = ['SliceNumber', 'ClusterCount']
                            write = csv.writer(file1)
                            write.writerow(heading)
                            write.writerows(outputList)

                        clusterCount.append(localCount-1)
                    name_idx+=1 



