import tensorflow
import numpy

from keras.models  import load_model

class NeuralNetworkModel:

    def __init__(self, modelToUse):
        self.model = load_model('CancerDetectionModel.h5')
        
        if (modelToUse == 0):
            self.model = load_model('TransferLearningCancerDetectionModel.h5')

    def process_image(self, imagePath):
        img        = tensorflow.keras.utils.load_img(imagePath, target_size=(128, 128))
        img_tensor = tensorflow.keras.utils.img_to_array(img)                  
        img_tensor = numpy.expand_dims(img_tensor, axis=0)        
        return img_tensor

    def predict(self, imagePath):
        image = self.process_image(imagePath)
        prediction = self.model.predict(image)
        if prediction > 0.5: return 'Healthy'
        else: return 'BrainTumor'
        