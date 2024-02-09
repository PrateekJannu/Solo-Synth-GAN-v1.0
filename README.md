# Solo-Synth-GAN-v1.0
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

This is the open-source repository for the project "Solo-Synth GAN" which is one of the latest zero shot generative adversarial network


# Single-Image GANs: Improved Training Techniques

For a concise summary of our paper, please refer to our [blog post](https://github.com/PrateekJannu/Solo-Synth-GAN-v1.0).(Will be updated once paper is published)

## Additional Data

You can find supplementary material, including videos, in the [Supplementary Material](https://github.com/PrateekJannu/Solo-Synth-GAN-v1.0) section.

## Overview

In this work, we propose and examine new techniques for training Generative Adversarial Networks (GANs) on a single image. Our approach involves training the model iteratively on different resolutions of the original image, gradually increasing resolution as training progresses. As the resolution increases, we augment the generator's capacity by adding additional convolutional layers. At each stage, only the most recently added convolutional layers are trained with a higher learning rate, while previously existing layers are trained with a smaller learning rate.

## Model Architecture

Our model architecture is based on PyTorch 1.1.0 and Python 3.8. For installation, please run:

```bash
pip install -r requirements.txt
```

## Unconditional Generation (GPU is a must and required for training and generation)

To train a model with default parameters from our paper(to be published), execute:

```bash
python main.py --gpu 0 --train_mode generation --input_name Images/marinabaysands.jpg
```

Training a single model typically takes about 8 minutes on a NVIDIA® V100 Tensor Core.

| Original Image | Generated Samples |
| --- | --- |
| ![Original](Images/marinabaysands.jpg) | ![Original](Examples/gen_sample_0.jpg) ![Original](Examples/gen_sample_10.jpg)  ![Original](Examples/gen_sample_18.jpg) ![Original](Examples/gen_sample_0.jpg)|
|  |  |

## Customization Options

To modify learning rate scaling or the number of trained stages, you can adjust parameters as follows:

```bash
python main.py --gpu 0 --train_mode generation --input_name Images/colusseum.png --lr_scale 0.5
```

or

```bash
python main.py --gpu 0 --train_mode generation --input_name Images/colusseum.png --train_stages 7
```


## Unconditional Generation (Arbitrary Sizes)

For generating images of arbitrary sizes, use the following command:

```bash
python main.py --gpu 0 --train_mode retarget --input_name Images/colusseum.png
```

## Image Animation (Coming Soon!)

To train an animation model or generate GIFs from a trained model, refer to the provided commands in the repository.

## Harmonization and Editing(Coming Soon!)

Instructions for training models for harmonization and editing tasks, as well as fine-tuning and evaluation, are included in the repository.

## Additional Data(Coming Soon!)

The `User-Studies` folder contains raw images used for conducting user studies.

## Acknowledgements
---
For more details, please refer to the [paper, published soon](https://github.com/PrateekJannu/Solo-Synth-GAN-v1.0) and feel free to reach out with any questions or feedback!
