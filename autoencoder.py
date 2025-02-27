
'''
Autoencoder. 

TODO list:
    - create init for class autoencoder.
        = 
    - Encoder 
        = build 
        = summary 
        = Convolutional layers 
        = bottleneck

    - Decoder 
        ...
'''

from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Conv2D, ReLU, BatchNormalization, \
    Flatten, Dense
from tensorflow.keras import backend as K

class Autoencoder:
    '''
    Autoencoder represents a Deep Convolutional autoencoder architecture with
    mirrored encoder and decoder. 
    '''

    def __init__(self, 
                 input_shape:tuple[int,int,int],
                 conv_filters:tuple[int,...],
                 conv_kernels:tuple[int,...],
                 conv_strides:tuple[int,...],
                 latent_space_dim:int):
         
        
        # assign parameters to the classes attributes.  
        self.input_shape = input_shape              #[ 28, 28, 1] minist 
        self.conv_filters = conv_filters            # [2,4,8] 
        self.conv_kernels = conv_kernels            # [3,5,3] 
        self.conv_strides = conv_strides            # [1,2,2]  
        self.latent_space_dim = latent_space_dim 

        self.encoder = None 
        self.decoder = None 
        self.model = None 

        # Assign private attributes 
        self._num_conv_layers:int = len(conv_filters) 
        self._shape_before_bottleneck= None 

        self._build() # TODO



    ### Class methods

    def summary(self):
        self.encoder.summary()


    ### private methods
    def _build(self):
        self._build_encoder() # TODO
#        self._build_decoder() # TODO
#        self._build_model()   # TODO


    def _build_encoder(self, name:str = 'encoder'):
        encoder_input = self._add_encoder_input() 
        conv_layers   = self._add_conv_layers(encoder_input)
        bottleneck    = self._add_bottleneck(conv_layers) 
        self.encoder  = Model(encoder_input, bottleneck, name=name) 

    def _add_encoder_input(self):
        return Input(shape=self.input_shape, name="encoder_input")

    def _add_conv_layers(self, encoder_input):
        """Create all convolutional blocks in encoder."""
        x = encoder_input
        for layer_index in range(self._num_conv_layers):
            x = self._add_conv_layer(layer_index, x)
        return x

    def _add_conv_layer(self, layer_index,x):
        '''
            conv 2d + ReLU + batch normlization. 
        ''' 
        layer_number = layer_index +1 
        conv_layer = Conv2D(
                filters=self.conv_filters[layer_index],
                kernel_size=self.conv_kernels[layer_index],
                strides=self.conv_strides[layer_index],
                padding ="same",
                name=f'encoder_conv_layer_{layer_number}'
        )
        x =conv_layer(x)
        x = ReLU(name=f'encoder_relu_{layer_number}')(x)
        x = BatchNormalization(name=f'encoder_bn_{layer_number}')(x)
        return x 

    def _add_bottleneck(self,x):
        '''
            flatten data and add bottleneck
        '''
        # get dimension for the decoder part
        self._shape_before_bottleneck = K.int_shape(x)[1:] # 
        x = Flatten()(x)
        x = Dense(self.latent_space_dim, name='encoder_output')(x)
        return x



if __name__ == '__main__':
    autoencoder = Autoencoder(
            input_shape=(28,28,1),
            conv_filters=(32,64,64,64), 
            conv_kernels=(3,3,3,3),
            conv_strides=(1,2,2,1),
            latent_space_dim=2 
    ) 
    autoencoder.summary()
