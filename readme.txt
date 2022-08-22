Automatic Bird Marker using YOLOv5

System Requirements: Python 3 and above with virtualenv installed if not use the command below to install.

        Linux/MacOS: python3 -m pip install --user virtualenv
        Windows: py -m pip install --user virtualenv
        Anaconda: conda install -c anaconda virtualenv


Step 0: Navigate to 'bird_marker' directory and create the virtual environment by running the command below.

        Linux/MacOS:  python3 -m venv marker
        Windows: py -m venv marker
        Anaconda: conda create -n marker pip

        Now 'marker' virtual environment is created, activate it using command below.

        Linux/MacOS: source marker/bin/activate
        Windows cmd: marker\Scripts\activate.bat
        Windows PowerShell: marker\Scripts\Activate.ps1
        Windows PowerShell Core: marker/bin/Activate.ps1
        Anaconda: conda activate marker

        Now install required packages using $ pip install -r requirements.txt or $ pip3 install -r requirements.txt

Running the model:

First run $ python clear_all.py to delete the delete.txt in folders.

Step 1: Paste the images to be marked in the images folder.
        CAUTION: There are already some test images in the folder, delete them before pasting new images.

Step 2: Run the detect.py script: $ python3 detect.py 
        The generated csv files of YOLOv5 output are in 'labels' folder

Step 3: There are theree different scripts for marking: 

        i) $ python mark_all.py (very fast)
                All images will be marked without any verification.

        ii) $ python3 mark_image.py (fast)
                Every image will be shown with all markers for verification, press 'y' to save it and its labels 
                and press 'n' twice to discard it.
                Discarded images will be copied to 'rejected' folder.
        
        iii) $ python3 mark_label.py (slow)
                Every image with each label marked at a time will be shown with window name same as the label to be verified.

                To save the label press 'y' and to mark the label manualy press 'n' twice, you enter marking mode 
                then mark manually by left mouse click and press 'y' to save it.
                PS: Blue markers are temporary markers, red ones are actual saved markers

                Finally entire image will be shown with the labels, press 'y' to save it press 'n' twice to skip.
             

        The 'output' folder will have results, which has two sub folders 'labelled_images' with marked images 
        and 'image_labels' with csv files of labels. 

        The input images are transferred to images_done folder and yolo generated labels to lables_done folder.

Step 4: Copy the 'output' folder onto your local computer. $ python3 clear_all.py can be run to clear output, labels, rejected
        images_done and label_done folders.

        Follow the same steps for new images.


CAUTION: DO NOT DELETE ANY FILES IN 'YOLOv5-master' AND 'yolo_full' !