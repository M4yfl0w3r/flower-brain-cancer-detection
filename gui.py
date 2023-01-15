import PySimpleGUI as gui

from io         import BytesIO
from pathlib    import Path
from PIL        import Image, UnidentifiedImageError


def image_to_data(image):
    with BytesIO() as output:
        image.save(output, format = 'PNG')
        data = output.getvalue()
    return data

class Gui:
    
    def __init__(self):
        gui.theme('DarkBlue')

        self.size = 640, 480

        self.layout = [[gui.Text('Choose image file')],
                       [gui.Input(expand_x = True, key = 'FilePath'), gui.Button('Browse')],
                       [gui.Text('', expand_x = True, key = 'Status')],
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
                    self.window['Status'].update('Cannot identify image file!')
                    continue

                imageWidth, imageHeight = image.size
                scale = min(640 / imageWidth, 480 / imageHeight, 1)
                
                if scale != 1:
                    image = image.resize((int(imageWidth * scale), int(imageHeight * scale)))
                
                data = image_to_data(image)
                self.window['Image'].update(data = data, size = self.size)