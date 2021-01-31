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
import errno
import imghdr
from itertools import islice
import operator
import os
import shutil

import instaloader
import numpy as np
from PIL import Image
import scipy.cluster
import scipy.misc
from sklearn.cluster import KMeans

class ColourPalette:
    
    def __init__(self, path, num_clusters=5, instagram=False, user=None, password=None, num_images=9):
        ''' Constructor
        '''
        self.path = path
        self.num_clusters = num_clusters
        self.instagram = instagram
        self.user = user
        self.password = password
        self.num_images = num_images
        
    def _from_instagram(self):
        ''' Downloads [num_images] latest images from an instagram profile.
        User and password may be needed to download pictures from private profiles.
        '''
        if not self.instagram:
            raise Exception("_from_instagram() cannot be invoked with current context. Set instagram=True.")
        
        # Get instance
        L = instaloader.Instaloader(save_metadata=False, download_comments=False, post_metadata_txt_pattern="")
        
        # If credentials were provided, login to Instagram
        if self.user is not None and self.password is not None:
            L.login(self.user, self.password)
        
        # Creates a profile object for the specified target
        profile = instaloader.Profile.from_username(L.context, self.path)
        
        # Adjusting the number of downloadable images
        post_iter = profile.get_posts()
        
        # Delete contents of ./tmp directory in case it exists
        self.path = "tmp"
        if os.path.isdir('./tmp'):
            shutil.rmtree('./tmp') 
            
        # Downloading only [num_images] images
        for post in islice(post_iter, self.num_images):
            L.download_post(post, "tmp")
        
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
        if self.instagram:
            self._from_instagram()

        codes, counts = self._clusterize()
        # Sorts all colours by appearance count
        codes = [k for k, v in sorted(zip(codes, counts), key=operator.itemgetter(1))][::-1]
        counts = np.sort(counts)[::-1]
            
        return codes, counts