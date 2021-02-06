''' COLOUR PALETTE APP
    ----------------------
    @author: F. Javier Muñoz Navarro, 2021
    CEO & Founder at Saoi Tech Solutions
    
    Follow us on LinkedIn: https://www.facebook.com/saoitech
    Follow me on Github: https://github.com/javiermunooz
    ---------------------- 
    
    @description: This simple Python-Tkinter app allows you to select a picture from
    your local file system and display an associated 6-colour palette.
    
    @usage:
    
    1. Execute the app
    2. Click on "Load file"
    3. Select a file from your machine. Might need to change the file type (bottom right).
    4. ¡You got your palette!
'''
import os
import random
from tkinter import Canvas
from tkinter import filedialog
from tkinter import simpledialog
import tkinter as tk

from PIL import ImageTk, Image

from colour_palette import ColourPalette

class MainApplication(object):
    def __init__(self, master, *args, **kwargs):
        ''' Application structure and GUI
        '''
        # Default image
        img = Image.open('./img/default-image.jpg')
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        
        # Master config
        self.master = master
        self._configure_gui()
        
        # Image
        self.panel = tk.Label(root, image = img)
        self.panel.image = img
        
        self.panel.grid(row = 0, column = 0,  columnspan=3, rowspan=3, padx = 5, pady = 5) 
        
        # Secondary label
        self.pal_label = tk.Label(root, text='Color Palette')
        
        self.pal_label.grid(row=3, column=0, columnspan=3, sticky='EW')
        
        # Colour Palette grid
        self.r1 = tk.Label(root, text='#ad261e', background='#ad261e', font=(None, -10))
        self.r2 = tk.Label(root, text='#09b2d2', background='#09b2d2', font=(None, -10))
        self.r3 = tk.Label(root, text='#1a73cd', background='#1a73cd', font=(None, -10))
        self.r4 = tk.Label(root, text='#fcfdfc', background='#fcfdfc', font=(None, -10))
        self.r5 = tk.Label(root, text='#c79437', background='#c79437', font=(None, -10))
        self.r6 = tk.Label(root, text='#1f232c', background='#1f232c', font=(None, -10))
        
        self.r1.grid(row=4, column=0, sticky='EW')
        self.r2.grid(row=4, column=1, sticky='EW')
        self.r3.grid(row=4, column=2, sticky='EW')
        self.r4.grid(row=5, column=0, sticky='EW')
        self.r5.grid(row=5, column=1, sticky='EW')
        self.r6.grid(row=5, column=2, sticky='EW')
        
        # Buttons
        self.greet_button = tk.Button(master, text="Load Image", command=self._process_img)
        self.insta_button = tk.Button(master, text="Load Insta", command=self._process_insta)
        self.close_button = tk.Button(master, text="Close", command=master.quit)
        
        self.greet_button.grid(row = 0, column = 5, sticky = 'E') 
        self.insta_button.grid(row = 1, column = 5, sticky = 'E') 
        self.close_button.grid(row = 2, column = 5, sticky = 'E') 

    def _to_tuple(self,a):
        ''' Converts an ndarray into a tuple of ints
        '''
        try:
            return tuple(a.astype(int))
        except TypeError:
            return a
    
    def _from_rgb(self,rgb):
        ''' Translates an rgb tuple of int to a tkinter friendly color code
        '''
        return "#%02x%02x%02x" % rgb
    
    def _get_palette(self, filename, instagram=False):
        ''' Finds the colour palette of a given picture
        '''
        cp = ColourPalette(filename, 6, instagram)
        codes = cp.colour_palette()[0]
        return codes
        
    def _load_file(self):
        ''' Loads a JPEG or PNG picture using a Windows dialog
        '''
        fname = filedialog.askopenfilename(filetypes=(("JPEG", "*.jpeg;*.jpg"),
                                           ("PNG", "*.png"),
                                           ("All files", "*.*") ))
        return fname
        
    def _process_img(self):
        ''' Reads, resizes and finds the colour pallete of an image.
        Modifies all 6 colour labels in the main GUI according to the colour palette.
        '''
        i = 0
        x = self._load_file()

        if x is not '':
            # Display image
            self.img2 = Image.open(x)
            self.img2 = self.img2.resize((250, 250), Image.ANTIALIAS)
            self.img2 = ImageTk.PhotoImage(self.img2)
            self.panel.configure(image=self.img2)
            self.panel.image=self.img2
            
            # Show colour palette
            codes = self._get_palette(x)
            objs  = [self.r1, self.r2, self.r3, self.r4, self.r5, self.r6]
            for code in codes:
                code = code[:3]
                code = self._from_rgb(self._to_tuple(code))
                objs[i].config(bg=code, text=code)
                i += 1
        
    def _process_insta(self):
        ''' Downloads the 5 latest images from a public instagram profile and finds their colour palette.
        Modifies all 6 colour labels in the main GUI according to the colour palette.
        '''
        i = 0
        handle = simpledialog.askstring("Input", "Enter your instagram handle", parent=root)
        
        if handle is not None:       
            # Show colour palette
            codes = self._get_palette(handle, instagram=True)
            print(codes)
            objs  = [self.r1, self.r2, self.r3, self.r4, self.r5, self.r6]
            for code in codes:
                code = code[:3]
                code = self._from_rgb(self._to_tuple(code))
                objs[i].config(bg=code, text=code)
                i += 1
                
            random_image = os.path.join('tmp', random.choice(os.listdir('tmp'))).replace('\\','/')
            # Display image
            self.img2 = Image.open(random_image)
            self.img2 = self.img2.resize((250, 250), Image.ANTIALIAS)
            self.img2 = ImageTk.PhotoImage(self.img2)
            self.panel.configure(image=self.img2)
            self.panel.image=self.img2
            
    def _configure_gui(self):
        ''' Initial config
        '''
        self.master.title("Colour Palette")
        self.master.geometry("400x400")
        self.master.resizable(True, True)
        
        
        
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()