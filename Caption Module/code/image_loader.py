#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
import scipy.misc


class Image_loader(object):
    def __init__(self,mean=None):
        if mean == None:
            self.mean_image = np.zeros((3,1,1))
        elif mean == "imagenet":
            mean_image = np.ndarray((3, 224, 224), dtype=np.float32)
            mean_image[0] = 103.939
            mean_image[1] = 116.779
            mean_image[2] = 123.68
            self.mean_image = mean_image
        else:
            self.mean_image = mean
 
    def load(self,image_path,image_w=224,image_h=224,expand_batch_dim=True):
        image = Image.open(image_path).convert('RGB')
        return self.resise(image,image_w,image_h,expand_batch_dim)

    def resise(self,image,image_w=224,image_h=224,expand_batch_dim=True):
        w, h = image.size
        if w > h:
            shape = (image_w * w // h, image_h)
        else:
            shape = (image_w, image_h * h // w)
        x = (shape[0] - image_w) // 2
        y = (shape[1] - image_h) // 2
        pixels = np.asarray(image.resize(shape).crop((x, y, x + image_w, y + image_h))).astype(np.float32)
        pixels = pixels[:,:,::-1].transpose(2,0,1)
        pixels -= self.mean_image
        if expand_batch_dim:
            return pixels.reshape((1,) + pixels.shape)
        else:
            return pixels

    def save(self,np_image,file_path):
        np_image=np_image.transpose(1,2,0)[:,:,::-1]
        scipy.misc.imsave(file_path, np_image)

