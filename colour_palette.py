''' COLOUR PALETTE LIBRARY
    ----------------------
    @author: F. Javier Muñoz Navarro, 2021
    CEO & Founder at Saoi Tech Solutions
    
    Follow us on LinkedIn: https://www.facebook.com/saoitech
    Follow me on Github: https://github.com/javiermunooz
    ---------------------- 
    
    @description: This simple Python library provides a colour palette for any given JPEG
    or PNG image. This is achieved by reducing the number of colours in an image via
    KMeans clustering.
    
    @usage:
    
    cp = ColourPalette(path='my_image.jpg', num_clusters=5)
    codes, counts = cp.colour_palette()
'''

import binascii
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import scipy.misc
import operator
import scipy.cluster
import os
import errno
import imghdr
import instaloader

class ColourPalette:
    
    def __init__(self, path, num_clusters=5):
        ''' Constructor
        '''
        self.path = path
        self.num_clusters = num_clusters
        
    def _read_image(self, img=None):
        ''' Reads and reshapes an image
        '''
        if img is None:
            path = self.path
        else:
            path = img
        im = Image.open(path)
        im = im.resize((150,150)) # Improves efficiency
        ar = np.asarray(im)
        shape = ar.shape
        ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
        return ar
        
    def _clusterize(self, num_clusters=5):
        ''' KMeans clustering to reduce the number of colours to num_clusters
        '''
        start = True
        
        ''' Checks if the provided path is a directory or a file
        If it is a directory, all images are processed
        '''
        if os.path.isdir(self.path):
            for img in os.listdir(self.path):
                img = os.path.join(self.path,img)
                
                # Check if it is a proper image
                if imghdr.what(img) not in ['jpg', 'jpeg', 'png']:
                    continue
                
                ar_prov = self._read_image(img=img)
                
                if start:
                    # Initializing the multiple-image array
                    ar = ar_prov
                    start = False
                else:
                    # Concatenate all images
                    ar = np.concatenate((ar, ar_prov), axis=0)
                    
        elif os.path.isfile(self.path):
            # Check if file is a valid image
            if imghdr.what(self.path) not in ['jpg', 'jpeg', 'png']:
                raise Exception(self.path + 'is not a valid image!')
            
            ar = self._read_image()
        else:
            # Raising an error in case such file was not found
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.path)
        
        # Clustering images by colour
        codes, dist = scipy.cluster.vq.kmeans(ar, self.num_clusters)
        vecs, dist = scipy.cluster.vq.vq(ar, codes)
        counts, bins = np.histogram(vecs, len(codes))
        return codes, counts
        
    def most_common(self):
        ''' Returns current image's most common colour
        '''
        codes, counts = self._clusterize()
        index_max = np.argmax(counts) # finds most frequent
        peak = codes[index_max]
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        return peak, colour
    
    def colour_palette(self):
        ''' Returns current image's colour palette
        '''
        codes, counts = self._clusterize()
        # Sorts all colours by appearance count
        codes = [k for k, v in sorted(zip(codes, counts), key=operator.itemgetter(1))][::-1]
        counts = np.sort(counts)[::-1]
            
        return codes, counts