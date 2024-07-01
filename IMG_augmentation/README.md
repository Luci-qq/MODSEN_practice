# ImageAugmentationApp

[Go back](../README.md)

An application for image augmentation.
List of supported augmentations:

- Crop
- Rotate
- Contrast
- Brightness
- Saturation
- Noise
- Shift
- Shear
- Stretch
- Random Crop
- Add text

## Contents

- [Technologies](#id_technologies)
- [Getting Started](#id_installation)

<a id='id_technologies'></a>

## Technologies

- [Kivy](https://kivy.org/)
- [Kivymd](https://kivymd.readthedocs.io/en/latest/index.html)
- [OpenCV](https://opencv.org/)
- [Pillow](https://python-pillow.org/)

<a id='id_installation'></a>

## Installation and Running

1. Create a virtual environment:

```sh
python -m venv venv
```

2.  Activate the virtual environment:

- Windows:

```sh
.\venv\Scripts\activate
```

- macOS и Linux:

```sh
source venv/bin/activate
```

3. Install dependencies:

```sh
pip install -r requirements.txt
```

4. Run the application:

```sh
python main.py
```
