#this repository is able to create mask images from single .json format
import json, os, glob
from PIL import Image, ImageDraw
import numpy as np

#see .json file format

dataset_path = "newdataset"
with open((os.path.join(dataset_path,"vgg.json"))) as json_file:
    labels = json.load(json_file)
    
labels
-------------------------
class_dict = {'labels':1}

#upload your .json file/ it can be in any file directory
json_file = 'newdataset/vgg.json'
all_labels = json.load(open(json_file))

#print label keys

print(all_labels.keys())

#define an image here and print it's keys
rawfile = 'image1.png'
print(all_labels[rawfile].keys())

def get_data(data):
    X = []; Y = []; L=[] #pre-allocate lists to fill in a for loop
    for k in data['regions']: #cycle through each polygon
        # get the x and y points from the dictionary
        X.append(data['regions'][k]['shape_attributes']['all_points_x'])
        Y.append(data['regions'][k]['shape_attributes']['all_points_y'])
        L.append(data['regions'][k]['region_attributes']['label'])
    return Y,X,L #image coordinates are flipped relative to json coordinates
    
X, Y, L = get_data(all_labels[rawfile])

image = Image.open(rawfile)

nx, ny,nz= np.shape(image)

#now define masks

def get_mask(X, Y, nx, ny, L, class_dict):
    # get the dimensions of the image
    mask = np.zeros((nx,ny))

    for y,x,l in zip(X,Y,L):
        # the ImageDraw.Draw().polygon function we will use to create the mask
        # requires the x's and y's are interweaved, which is what the following
        # one-liner does
        polygon = np.vstack((x,y)).reshape((-1,),order='F').tolist()

        # create a mask image of the right size and infill according to the polygon
        if nx>ny:
            x,y = y,x
            img = Image.new('L', (nx, ny), 0)
        elif ny>nx:
           #x,y = y,x
           img = Image.new('L', (ny, nx), 0)
        else:
            img = Image.new('L', (nx, ny), 0)
        ImageDraw.Draw(img).polygon(polygon, outline=0, fill=1)
        # turn into a numpy array
        m = np.flipud(np.rot90(np.array(img)))
        try:
            mask[m==1] = class_dict[l]
        except:
            mask[m.T==1] = class_dict[l]  

    return mask
    
 mask = get_mask(X, Y, nx, ny, L, class_dict)
 
 #rescales an input dat between mn and mx
 def rescale(dat,mn,mx):
    
    m = min(dat.flatten())
    M = max(dat.flatten())
    return (mx-mn)*(dat-m)/(M-m)+mn
    
 ##now the below code will automaticly save the images as image1_label.jpg/ this part will turn all of the images. 

for rawfile in all_labels.keys():

    X, Y, L = get_data(all_labels[rawfile])

    image = Image.open('image1.png') # be careful about image definition it will take it where the code defined. 

    nx, ny,nz= np.shape(image)

    mask = get_mask(X, Y, nx, ny, L, class_dict)
    mask = Image.fromarray(rescale(mask,255,0)).convert('L')

    mask.save(rawfile.replace('.png','_label.jpg'), format='PNG')
 
 #see the pic
 
 mask
 
