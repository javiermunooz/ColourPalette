# Colour Palette

_This simple Python-Tkinter app allows you to select a picture from your local file system and display an associated 6-colour palette. You can also make use of the ColourPalette module as an API for your own application._

_ColourPalette applies KMeans algorithm on a picture in order to extract its most relevant colours._

## How to start 🚀

_Naturally, first thing you need to do is clone this repository!_

```
git clone https://github.com/javiermunooz/ColourPalette.git
cd ColourPalette
```

Check out **Installation** to learn more about how to make this application work.


### Prerequisites 📋

_You will need Python 3.6.8 or later. This application has only been tested on Windows 10, so there is no guarantee it will work on a different platform._


### Installation 🔧

_I would recommend that you set up a Python virtual environment in order to run this application without interfering with your current Python environment_

_Execute the following commands_

```
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

_Once finished, everything will be ready to launch the app!_ 

_When you are done with ColourPalette, you can deactivate the virtual environment by simply typing_

```
deactivate
```

## Running ColourPalette ⚙️

_You will simply need to launch the app.py file_

```
python app.py
```

_In case you want to build your own application, here is an example of how to use ColourPalete:_

```
cp = ColourPalette(path='my_image.jpg', n_clusters=5)

# Gets a N-colour palette
codes, counts = cp.colour_palette()

# Gets the most frequent colour in your picture
peak, colour = cp.most_common()
```

_Since version v0.1.1 multi-picture analysis is supported. You can find a colour palette for set of pictures by specifying the path to a folder containing such images in the path parameter_

```
cp = ColourPalette(path='./mydir/', n_clusters=5)

# Gets a N-colour palette
codes, counts = cp.colour_palette()
```

_From version v0.2.0 you can also find the colour palette of any instagram profile. Set intagram=True and path parameter to the target handle_

```
cp = ColourPalette(path='handle', n_clusters=5, instagram=True, num_images=9)

# Gets a N-colour palette
codes, counts = cp.colour_palette()
```

_Please note this will only work for public profiles. If you want to work with private profiles, you will need to follow that account and add the user and password parameters to ColourPalette initializer._

```
cp = ColourPalette(path='handle', n_clusters=5, instagram=True, num_images=9, login='yourlogin', password='yourpass')

# Gets a N-colour palette
codes, counts = cp.colour_palette()
```


### License 📄

_This project was built under MIT license, which basically means do whatever you want but don't forget to credit the original author! A short @javiermunooz will do the trick._

Check out [LICENSE.md](LICENSE.md) for details.


## Contributing 🖇️

Pull requests are more than welcome to help improve this application. Some things to work on next:

- GUI improvements.
- Displaying palette's RGB values.
- Allowing users to copy colour codes to their clipboard.
- Colour palletes of more/less than 6 colours.

---
⌨️ With ❤️ by [javiermunooz](https://github.com/javiermunooz) 
