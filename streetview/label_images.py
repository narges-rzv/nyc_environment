import torch
from torch import nn
from torch.nn.parameter import Parameter
from torch.autograd import Variable

import torchvision.models as models

import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt
import json, string
import pickle
from multiprocessing import Pool


class streetview_labler():
    def __init__(self, imagenet_jsonFile='../imagenet_class_index.json'):
        self.model = models.resnet18(pretrained=True)
        self.preprocessFn = transforms.Compose([transforms.Scale(256),
                                   transforms.CenterCrop(224),
                                   transforms.ToTensor(),
                                   transforms.Normalize(mean = [0.485, 0.456, 0.406],
                                                        std=[0.229, 0.224, 0.225])])
        with open(imagenet_jsonFile) as f:
            self.imagenetClasses = {int(idx): entry[1] for (idx, entry) in json.load(f).items()}
        self.model.eval()

    def label_image(self, fname):
        with Image.open(fname).convert('RGB') as image:
            inputVar =  Variable(self.preprocessFn(image).unsqueeze(0))
            predictions = self.model(inputVar)

            probs, indices = (-nn.Softmax()(predictions).data).sort()
            probs = (-probs).numpy()[0][:10]; indices = indices.numpy()[0][:10]
            preds = [self.imagenetClasses[idx] + ': ' + str(prob) for (prob, idx) in zip(probs, indices)]

            fname_labels= fname.replace('.jpg', '.preds.pkl')
            pickle.dump(file=open(fname_labels, 'wb'), obj=preds, protocol=-1)
            fname_plot = fname.replace('.jpg', '.pred_plt.png')
            plt.title('\n'.join(preds))
            plt.imshow(image)
            plt.tight_layout()
            plt.savefig(fname_plot, bbox_inches='tight')
            plt.close()
            print(fname_plot)
            

    def parallel_labeler(self, listOfFnames):
        p = Pool(17)
        p.map(self.label_image, listOfFnames)

