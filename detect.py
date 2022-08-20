import torch
import os
from PIL import Image
import time

start = time.process_time()

model_path = os.path.join(os.getcwd(), 'yolo_full', 'weights', 'best.pt' ) #path to trained model
print('model path: ', model_path)
model = torch.hub.load('yolov5-master', 'custom', path = model_path, source = 'local') #loading the model
# model.conf = 0.75
# model.iou = 0.45

for file in sorted(os.listdir(os.path.join(os.getcwd(), 'images'))):    #iterating through all the images in 'images' folder

    file_path = os.path.join(os.getcwd(), 'images', file)                #path to image
    ext = file.split(".")
    save_file = os.path.join(os.getcwd(), 'labels', str(ext[0]) + ".csv") #path to save csv
    img = Image.open(file_path)                                           #loading the image
    results = model(img, size=640)                                       #running image through model   

    #results.save()          #uncomment this if you want to save the image with bounding box (slower execution)
                             #path will be displayed after run is complete, delete the folders later

    results.pandas().xyxy[0].to_csv(save_file)      #saving label files as csv
    print(ext[0])                                   #display files processed

end_time = time.process_time() - start
print('Time elapsed: ', end_time) 