import pandas as pd
import cv2
import os
import shutil

anno_path = 'labels'
img_path = 'images'


img_width = 1280
img_height = 960
red = [0,0,255]
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
thickness = 2
font_colour = (255, 255, 255)
conf_thres = 0.7


def convert(xmin, ymin, xmax, ymax):

    x = (xmin + xmax)/2.0 - 1
    y = (ymin + ymax)/2.0 - 1

    return (x,y)


def mark_image(annopath, imgpath, file):

    COLUMN_NAMES = ['filename', 'label', 'x', 'y', 'confidence']
    df = pd.DataFrame(columns=COLUMN_NAMES)
    
    image = cv2.imread(imgpath)
    dta = pd.read_csv(annopath)

    for index, row in dta.iterrows():

        x_min = row['xmin']
        y_min = row['ymin']
        x_max = row['xmax']
        y_max = row['ymax']
        conf = row['confidence']
        labl = row['name']
        x_pt, y_pt = convert(x_min, y_min, x_max, y_max)
        if conf > conf_thres:
            org = (int(x_pt), int(y_pt))
            image = cv2.circle(image, org, radius=2, color=red, thickness=2)
            image = cv2.putText(image, labl, org, font, 
                    fontScale, font_colour, thickness, cv2.LINE_AA)
            row_data = pd.DataFrame({'filename': file, 'label': labl, 'x': x_pt, 'y': y_pt, 'confidence': conf}, index=[0])
            df = pd.concat([df, row_data])
        else:
            continue
        
    return image, df


for file in sorted(os.listdir(img_path)):
    f_name = os.path.splitext(file)[0]
    img_file = os.path.join(os.getcwd(), img_path, file)
    csv_file = os.path.join(os.getcwd(), anno_path, f_name + '.csv')
    img, labels = mark_image(csv_file, img_file, f_name)
    img_dest = os.path.join(os.getcwd(), 'output', 'labelled_images', f_name + '_labelled.png')
    cv2.imwrite(img_dest, img)
    csv_dest = os.path.join(os.getcwd(), 'output', 'image_labels', f_name + '_labels.csv')
    labels.to_csv(csv_dest)
    print(f_name)
    shutil.move(img_file,'images_done')
    shutil.move(csv_file, 'labels_done')

print('Open output folder for the results')
    
