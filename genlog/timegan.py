from TimeGAN.timegan import timegan
from TimeGAN.data_loading import real_data_loading, sine_data_generation

data_name = 'stock'
seq_len = 24

ori_data = real_data_loading(data_name, seq_len)

## Newtork parameters
parameters = dict()

parameters['module'] = 'gru'
parameters['hidden_dim'] = 24
parameters['num_layer'] = 3
parameters['iterations'] = 10000
parameters['batch_size'] = 128

# Run TimeGAN
generated_data = timegan(ori_data, parameters)
print('Finish Synthetic Data Generation')