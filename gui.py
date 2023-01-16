import PySimpleGUI as gui
import tensorflow  as tf
import numpy

from io            import BytesIO
from pathlib       import Path
from PIL           import Image, UnidentifiedImageError
from keras.models  import load_model

def image_to_data(image):
    with BytesIO() as output:
        image.save(output, format = 'PNG')
        data = output.getvalue()
    return data

class NeuralNetModel:

    def __init__(self):
        self.model = load_model('CancerDetectionModel.h5')

    def process_image(self, imagePath):
        img        = tf.keras.utils.load_img(imagePath, target_size=(128, 128))
        img_tensor = tf.keras.utils.img_to_array(img)                  
        img_tensor = numpy.expand_dims(img_tensor, axis=0)        
        img_tensor = img_tensor / 255.                    

        return img_tensor

    def predict(self, imagePath):
        image = self.process_image(imagePath)
        prediction = self.model.predict(image)
        print(prediction)

class Gui:
    
    def __init__(self):
        gui.theme('DarkBlue')
        self.width  = 640
        self.height = 480
        self.size   = self.width, self.height

        self.layout = [[gui.Text('Choose image file')],
                       [gui.Input(expand_x = True, disabled = True, key = 'FilePath'), gui.Button('Browse')],
                       [gui.Text('', expand_x = True, key = 'Status')],
                       [gui.Input(expand_x = True, disabled = True, key = 'Result'), gui.Button('Classify')],
                       [gui.Image(self.size, key = 'Image')]]

        self.window = gui.Window('Cancer detection', self.layout)

    def update(self):
        while True:

            event, _ = self.window.read()

            if event == gui.WIN_CLOSED:
                break

            if event == 'Browse':
                filePath = gui.popup_get_file('')

                if filePath == '':
                    continue

                self.window['Status'].update('')
                self.window['FilePath'].update(filePath)

                if not Path(filePath).is_file():
                    self.window['Status'].update('Image file not found!')
                    continue
                try:
                    image = Image.open(filePath)
                except UnidentifiedImageError:
                    self.window['Status'].update('This file type is not supported!')
                    continue

                dataImage = image_to_data(image)
                self.window['Image'].update(data = dataImage, size = self.size)

            if event == 'Classify':
                model = NeuralNetModel()
                self.window['Result'].update(model.predict(filePath))