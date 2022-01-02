# Traffic Sign Identification

## Dataset and Usage

- GTSRB Dataset: https://benchmark.ini.rub.de/gtsrb_dataset.html#Downloads
- Usage: `python traffic.py data_directory [model.h5]`
  - data_directory is where the dataset saved from above
  - [model.h5] is an optional parameter to save a model after training

## Process

### 1a. Convolution Layer Dropout: None
 - Dropout seems to be less effective in regularizing in convolution layers due to the low number of parameters to begin with.
 - Validation accuracy for each rate was averaged from three 15-epoch trials

| Rate        | Val Accuracy |
| :---:       | :----:       |
| 0.0         | 0.8740       |
| 0.1         | 0.8468       |
| 0.2         | 0.8005       |

### 1b. Pooling size: (2,2)
(3,3) is considerably faster but lowers accuracy too much, so (2,2) pooling was kept.

### 2a. Output activation function: Softmax
Softmax was used instead of sigmoid for the output activation function, since the former is used in multi-class problems, while the latter is used more in binary classification. We are classifying 43 classes of traffic signs, so softmax makes more sense. In addition, sigmoid sometimes experiences the exploding gradient problem, which leads to unstable updates to the network's model weights and hinders training ability.

### 2b. Batch Normalization
Adding batch normalization after a convolution layer allows the model to rapidly converge at a high accuracy and prevents a vanishing gradient during training. This change had the single greatest effect on the result. 

### 2c. Hidden Layer Dropout: 0.2
 - Higher dropout on hidden layers lead to lower training accuracy and higher loss, while low dropout can cause testing accuracy to suffer.
 - Based on the data table below, a dropout rate of 0.2 strikes the right balance
 - Validation accuracy for each rate was averaged from three 15-epoch trials

| Rate        | Val Accuracy |
| :---:       | :----:       |
| 0.0         | 0.9632       |
| 0.1         | 0.9702       |
| 0.2         | 0.9713       |
| 0.3         | 0.9647       |

### 3. Optimizer: Adamax

Adamax is a variant of the vanilla Adam optimizer that can work better on models with sparserly-updated parameters (embeddings).

| Type   | Val Accuracy (15 epochs)  |
| :---:  | :----:                    |
| Adam   | 0.9713                    |
| Nadam  | 0.9619                    |
| Adamax | 0.9803                    |

### 4a. Number of convolution layers: 2 (64-128)
| Configuration    | Val Accuracy (15 epochs) |
| ---:             | :----:                   |
| 3 (32-64-128)    | 0.9906                   |
| 2 (32-64)        | 0.9920                   |
| 1 (32)           | 0.9803                   |

### 4b. Number of nodes in hidden layer
 - Beyond 128 nodes in a hidden layer, the improvement is negligible.

| Configuration    | Val Accuracy (15 epochs) |
| :---:             | :----:                   |
| 64               | 0.9920                   |
| 128              | 0.9936                   |
| 256              | 0.9932                   |
| 512              | 0.9932                   |

### 5. Number of convolution layer nodes, number of hidden layers
- For these two hyperparameters, I used KerasTuner, an automated tuning library. This tool allows one to specify certain conditions for the search space, allowing for more efficient testing of different neural network configurations. 
- To minimize performance variance of a neural network, each configuration is run twice.
- The following conditions were used:
  - Convolution input layer has between 32 and 128 nodes (steps of 32)
  - Each subsequent convolutional layer has between size of input layer and 128 nodes (steps of 32)
  - The hidden input layer has between 32 and 256 nodes (steps of 32)
  - There are 1 to 3 hidden layers
  - Each subsequent hidden layer is half the size of the previous
- Each convolutional layer is paired with a batch normalization, and each hidden layer is paired with 0.2 dropout

- Results (raw data in "num_layers_and_units" directory)
  - Convolutional Input Layer: 96
  - Second Convolutional Layer: 256
  - Number of hidden layers: 1 (as confirmed by the top 5 trials)
  - Hidden Layer: 128

## Models by Stage

### Base Model: 87.40%
*Refer to parts 1a and 1b of 'Process' for changes that did not improve on the base model.*
* 32 Conv2D [relu]
* (2, 2) MaxPooling2D
* 64 Hidden Layer, dropout 0.1 [relu]
* 43 Output Layer [sigmoid]

### Model 2: 97.13%
*Refer to parts 2a, 2b, and 2c of 'Process' for details on the changes in the second model.*
* 32 Conv2D [relu]
* BatchNormalization
* (2, 2) MaxPooling2D
* 64 Hidden Layer, dropout 0.2 [relu]
* 43 Output Layer [softmax]

### Model 3: 98.03%
*Refer to part 3 of 'Process' for details on the changes in the third model.*
* 32 Conv2D [relu]
* BatchNormalization
* (2, 2) MaxPooling2D
* 64 Hidden Layer, dropout 0.2 [relu]
* 43 Output Layer [softmax]
* Optimizer: Adamax (instead of Adam)

### Model 4: 99.20%
*Refer to part 4 of 'Process' for details on the changes in the fourth model.*
* 32 Conv2D [relu]
* BatchNormalization
* (2, 2) MaxPooling2D
* 64 Conv2D [relu]
* BatchNormalization
* (2, 2) MaxPooling2D
* 128 Hidden Layer, dropout 0.2 [relu]
* 43 Output Layer [softmax]
* Optimizer: Adamax

### Model 5: 99.61%
* 96 Conv2D [relu]
* BatchNormalization
* (2, 2) MaxPooling2D
* 256 Conv2D [relu]
* BatchNormalization
* (2, 2) MaxPooling2D
* 128 Hidden Layer, dropout 0.2 [relu]
* 43 Output Layer [softmax]
* Optimizer: Adamax
