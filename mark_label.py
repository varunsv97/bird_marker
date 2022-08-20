import pandas as pd
import cv2
import os
import shutil

# img_path = 'images' ##Uncomment to run on all images
img_path = 'rejected'  #Comment to run on all images
anno_path = 'labels' 

red = [0,0,255] #marker colour
blue = [255, 0, 0]
font = cv2.FONT_HERSHEY_SIMPLEX #label font
fontScale = 1 #label font size
thickness = 2 #label font thickness
font_colour = [0,255,0] #label font colour
font_colour_tmp = [0,255,255]

conf_thres = 0.7 #confidence threshold for markers(0.7 recommended)

def convert(xmin, ymin, xmax, ymax): #function to get centroid of bounding box

    x = (xmin + xmax)/2.0 - 1
    y = (ymin + ymax)/2.0 - 1

    return (x,y)

def save(im, dfr, name): #function to save marked image and label files

    img_dest = os.path.join(os.getcwd(), 'output', 'labelled_images', name + '_labelled.png')
    cv2.imwrite(img_dest, im)
    csv_dest = os.path.join(os.getcwd(), 'output', 'image_labels', name + '_labels.csv')
    dfr.to_csv(csv_dest)


def mark_image(annopath, imgpath, file): #function to mark the images

    COLUMN_NAMES = ['filename', 'label', 'x', 'y', 'confidence']
    df = pd.DataFrame(columns=COLUMN_NAMES) #creating an empty dataframe to store marker points

    image = cv2.imread(imgpath) #loading image
    image_tmp = image.copy()
    dta = pd.read_csv(annopath) #loading labels

    for index, row in dta.iterrows(): #iterating through all the labels

        x_min = row['xmin']
        y_min = row['ymin']
        x_max = row['xmax']
        y_max = row['ymax']
        conf = row['confidence']
        labl = row['name']

        x_pt, y_pt = convert(x_min, y_min, x_max, y_max) #getting centroid of bounding box

        def drawCircle(event, x, y, flags, param): #function to draw circle at mouse point

            global row_data_

            if event == cv2.EVENT_LBUTTONDOWN: #event at left double click
                
                org_ = (x, y)
                
                cv2.circle(image, org_, radius=2, color=red, thickness=2)
                cv2.putText(image, labl, org_, font, 
                            fontScale, font_colour, thickness, cv2.LINE_AA)

                cv2.circle(image_tmp, org_, radius=2, color=red, thickness=2)
                cv2.putText(image_tmp, labl, org_, font, 
                            fontScale, font_colour, thickness, cv2.LINE_AA)

                cv2.imshow(labl, image)
                row_data_ = pd.DataFrame({'filename': file, 'label': labl, 'x': x, 'y': y, 'confidence': 1.0}, index=[0])
                

        if conf > conf_thres: #limiting labels by their confidence value

            org = (int(x_pt), int(y_pt)) #convert co-ordinate points to integer
            image_tmp = cv2.circle(image_tmp, org, radius=2, color=blue, thickness=2) #marking point on image
            image_tmp = cv2.putText(image_tmp, labl, org, font, 
                    fontScale, font_colour_tmp, thickness, cv2.LINE_AA) #writing marker name on image

            cv2.imshow(labl+'_temp', image_tmp) #display image with marker

            if cv2.waitKey(0) == ord('y'): #condition for saving the marker

                image = cv2.circle(image, org, radius=2, color=red, thickness=2)
                image = cv2.putText(image, labl, org, font, 
                                    fontScale, font_colour, thickness, cv2.LINE_AA)
                image_tmp = cv2.circle(image_tmp, org, radius=2, color=red, thickness=2)
                image_tmp = cv2.putText(image_tmp, labl, org, font, 
                                fontScale, font_colour, thickness, cv2.LINE_AA)

                row_data = pd.DataFrame({'filename': file, 'label': labl, 'x': x_pt, 'y': y_pt, 'confidence': conf}, index=[0])
                df = pd.concat([df, row_data])
                cv2.destroyAllWindows()

            elif cv2.waitKey(0) == ord('n'):

                cv2.imshow(labl, image)
                cv2.setMouseCallback(labl, drawCircle)
                cv2.waitKey(0) == ord('y')
                df = pd.concat([df, row_data_])
                cv2.destroyAllWindows()

            else:

                continue

        else:

            continue

    return image, df



for file in sorted(os.listdir(img_path)): #iterating through all files in the folder

    f_name = os.path.splitext(file)[0]
    img_file = os.path.join(os.getcwd(), img_path, file)
    csv_file = os.path.join(os.getcwd(), anno_path, f_name + '.csv')
    img, labels = mark_image(csv_file, img_file, f_name)
    cv2.imshow(f_name, img)

    if cv2.waitKey(0) == ord('y'): #condition to save the image and labels file
        save(img, labels, f_name)
        cv2.destroyAllWindows()
        print('saved', f_name)
        shutil.move(img_file,'images_done')
        shutil.move(csv_file, 'labels_done')

    elif cv2.waitKey(0) == ord('n'): #condition to skip the image and labels file
        cv2.destroyAllWindows()
        print('rejected', f_name)
        
    else:

        continue



print('Open output folder for the results')
print('Open rejected folder for rejected images', 'run mark_label.py for labelling them')