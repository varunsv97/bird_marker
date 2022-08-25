import pandas as pd
import cv2
import os
import shutil

anno_path = 'labels' #path to labels
img_path = 'images' #path to images



red = [0,0,255] #marker colour
font = cv2.FONT_HERSHEY_SIMPLEX #label font
fontScale = 1 #label font size
thickness = 2 #label font thickness
font_colour = [0,255,0] #label font colour

conf_thres = 0.7 #confidence threshold for markers(0.7 recommended)


def convert(xmin, ymin, xmax, ymax): #function to get centroid of bounding box

    x = (xmin + xmax)/2.0 - 1
    y = (ymin + ymax)/2.0 - 1

    return (x,y)

def save(im, dfr, name): #function to save the image and labels file
    
    img_dest = os.path.join(os.getcwd(), 'output', 'labelled_images', name + '_labelled.png')
    cv2.imwrite(img_dest, im)
    csv_dest = os.path.join(os.getcwd(), 'output', 'image_labels', name + '_labels.csv')
    dfr.to_csv(csv_dest)


def mark_image(annopath, imgpath, file):

    COLUMN_NAMES = ['filename', 'label', 'x', 'y', 'confidence']
    df = pd.DataFrame(columns=COLUMN_NAMES)
    
    image = cv2.imread(imgpath)
    dta = pd.read_csv(annopath)
    label_list = []

    for index, row in dta.iterrows():

        conf = row['confidence']
        labl = row['name']

        if (labl not in label_list) and (conf >= conf_thres):

            x_min = row['xmin']
            y_min = row['ymin']
            x_max = row['xmax']
            y_max = row['ymax']

            x_pt, y_pt = convert(x_min, y_min, x_max, y_max)
            org = (int(x_pt), int(y_pt))

            image = cv2.circle(image, org, radius=2, color=red, thickness=2)
            image = cv2.putText(image, labl, org, font, 
                    fontScale, font_colour, thickness, cv2.LINE_AA)

            row_data = pd.DataFrame({'filename': file, 'label': labl, 'x': x_pt, 'y': y_pt, 'confidence': conf}, index=[0])
            df = pd.concat([df, row_data])
            
            label_list.append(labl)

        else:

            continue

    return image, df



for file in sorted(os.listdir(img_path)):
    f_name = os.path.splitext(file)[0]
    img_file = os.path.join(os.getcwd(), img_path, file)
    csv_file = os.path.join(os.getcwd(), anno_path, f_name + '.csv')
    img, labels = mark_image(csv_file, img_file, f_name)
    cv2.imshow(f_name, img)

    if cv2.waitKey(0) == ord('y'):
        save(img, labels, f_name)
        cv2.destroyAllWindows()
        print('saved', f_name)
        shutil.move(img_file,'images_done')
        shutil.move(csv_file, 'labels_done')

    elif cv2.waitKey(0) == ord('n'):
        cv2.destroyAllWindows()
        shutil.move(img_file, 'rejected')
        print('rejected', f_name)
        
    else:

        continue



print('Open output folder for the results')
print('Open rejected folder for rejected images', 'run mark_label.py for labelling them')