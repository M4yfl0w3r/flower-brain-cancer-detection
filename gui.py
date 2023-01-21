import PySimpleGUI as gui

from NeuralNetworkModel import NeuralNetworkModel
from io                 import BytesIO
from pathlib            import Path
from PIL                import Image, UnidentifiedImageError

def image_to_data(image):
    with BytesIO() as output:
        image.save(output, format = 'PNG')
        data = output.getvalue()
    return data

class Gui:
    
    def __init__(self):
        gui.theme('DarkBlue14')
        self.width  = 640
        self.height = 480
        self.size   = self.width, self.height
        
        self.modelChoice = ['Transfer learning model', 'My model']

        self.layout = [[gui.Text('Choose image file')],
                       [gui.Input(expand_x = True, disabled = True, key = 'FilePath'), gui.Button('Browse')],
                       [gui.Text('', expand_x = True, key = 'Status')],
                       [gui.Input(expand_x = True, disabled = True, key = 'Result'), gui.Button('Classify')],
                       [gui.Text('Choose a model'), gui.Combo([model for model in self.modelChoice], key = 'Model', expand_x = True)],
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
                model = NeuralNetworkModel(self.window['Model'].widget.current())
                self.window['Result'].update(model.predict(filePath))