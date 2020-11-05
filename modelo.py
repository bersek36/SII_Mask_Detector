from PIL import Image, ImageDraw, ImageFont
from sklearn.neighbors import KNeighborsClassifier
from networks import EmbeddingNet, TripletNet
import pickle
import random
from facenet_pytorch import MTCNN
import numpy as np
import torch
import cv2 
 ##
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
mtcnn = MTCNN(keep_all=True, device=device, margin = 40)

checkpoint = torch.load('MaskRecognition/models/checkpoint_tr.pth',map_location=device)
embedding_net = EmbeddingNet()
model = TripletNet(embedding_net).to(device)
model.load_state_dict(checkpoint['state_dict'])

emb_single = pickle.load( open( "MaskRecognition/models/emb_single_triplet.p", "rb" ) )
X = emb_single['X']
y = emb_single['y']
fnt = ImageFont.truetype("C:/Users/Bersek/Desktop/Proyecto/MaskRecognition/ARIALBD.TTF", 40)
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X, y)


def to_tensor(frame):

    fr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    fr= Image.fromarray(fr)
    #Process each face
    faces = mtcnn(fr)
    faces = faces.to(device)
    return faces, fr

def detect_and_predict_mask(faces, frame):

    if type(faces).__name__ != 'NoneType':
        boxes, probs = mtcnn.detect(frame)
        emb = model.embedding_net.forward(faces).detach().to('cpu').numpy()
        if emb.shape[0]==1:
            emb = emb.reshape(1, -1)
        yest = neigh.predict(emb)
    
    return yest, boxes

def labeled(frame, yest, boxes):

    colors = [(0,255,0),(255,0,0),(0,0,255)]
    labels = ["Ok", "No Mask" ,"Bad"]

    draw = ImageDraw.Draw(frame)
    for f,box in enumerate(boxes):
        (startX, startY, endX, endY) = box
        idx = random.randint(0,2)
        outline = colors[yest[f]]
        draw.text((startX,endY), labels[yest[f]], font=fnt, fill=outline)
        draw.rectangle(box.tolist(), outline=tuple(outline), width=6)
    frame = np.array(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    return frame