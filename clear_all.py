import os

imdir =  os.path.join(os.getcwd(), 'images_done')
lbdir = os.path.join(os.getcwd(), 'labels_done')
op_im_dir = os.path.join(os.getcwd(), 'output', 'labelled_images')
op_lb_dir = os.path.join(os.getcwd(),'output', 'image_labels')


def clear_dir(dir_path):
    for file in os.listdir(dir_path):
        os.remove(os.path.join(os.getcwd(), dir_path, file))

clear_dir(imdir) #clear images_done
clear_dir(lbdir) #clear labels_done
clear_dir(op_im_dir) #clear output images
clear_dir(op_lb_dir) #clear output labels
print('As good as new')