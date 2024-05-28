# Image Colorization
In this work, we assess the performance of various deep-learning architectures to colorize black-and-white images. We train three main models, a convolutional neural network (CNN), a U-Net, and a generative adversarial network (GAN). We implement three loss functions to understand their impact on the colorization properties. We evaluate the models’ performances using mean squared error (MSE), peak signal-to-noise ratio (PSNR), structural similarity index measure (SSIM), and Fréchet inception distance (FID) score. The results indicate that standard CNNs struggle to capture the color structure of images, whereas U-Nets achieve significantly better colorization, even with the same loss functions. GANs, although challenging to train, show comparable outcomes to those of the U-Net, but show potential for improvement.