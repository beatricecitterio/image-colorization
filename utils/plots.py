"""
plots.py

This module provides functions for visualizing LAB color channels and RGB images.

Authors: Diego Cerretti, Beatrice Citterio, Mattia Martino, Sandro Mikautadze
"""

import torch
import matplotlib.pyplot as plt
import numpy as np
from skimage.color import lab2rgb
from typing import Tuple

def plot_l(l_channel: torch.Tensor):
    """
    Plot the L channel of a Lab image.

    Args:
        l_channel (torch.Tensor): Tensor containing the L channel values. Size 1xHxW
    """
    l_channel = l_channel.squeeze()  # remove unnecessary dimension --> we now have shape [H, W] and not [1, H, W]
    plt.figure(figsize=(6, 6))
    plt.imshow(l_channel, cmap='gray')
    plt.axis('off')
    plt.show()

def plot_a(a_channel: torch.Tensor):
    """
    Plot the A channel of a Lab image.

    Args:
        a_channel (torch.Tensor): Tensor containing the A channel values. Size HxW
    """
    plt.figure(figsize=(6, 6))
    plt.imshow(a_channel, cmap='coolwarm')
    plt.axis('off')
    plt.show()

def plot_b(b_channel: torch.Tensor):
    """
    Plot the B channel of a Lab image.

    Args:
        b_channel (torch.Tensor): Tensor containing the B channel values. Size HxW
    """
    plt.figure(figsize=(6, 6))
    plt.imshow(b_channel, cmap='coolwarm')
    plt.axis('off')
    plt.show()

def plot_rgb(rgb_image: torch.Tensor):
    """
    Plot an RGB image.

    Args:
        rgb_image (torch.Tensor): Tensor containing the RGB image values. Size 3xHxW
    """
    rgb_image = rgb_image.permute(1, 2, 0)  # convert from CxHxW to HxWxC for plotting
    plt.figure(figsize=(6, 6))
    plt.imshow(rgb_image)
    plt.axis('off')
    plt.show()

def plot_ab(ab_channels: torch.Tensor, l_values=[20, 40, 80]):

    # Retrieve the A and B channels from the tensor
    a = ab_channels[0].cpu()
    b = ab_channels[1].cpu()

    for l_value in l_values:
        # Create an L channel tensor filled with the constant L value, shaped appropriately
        l = torch.full_like(a, l_value)  # Create a full tensor for L

        # Stack the L, A, B channels to form the complete LAB image tensor
        lab_image = torch.stack((l, a, b), dim=0)

        # Convert the tensor to a numpy array for further processing
        lab_image_np = lab_image.permute(1, 2, 0).numpy()

        # Denormalize the LAB values
        # L channel: Originally scaled to [0, 100] in the dataset preparation
        # A and B channels: Normalize from [-1, 1] (assumed here) back to [-127, 128]
        lab_image_np[:, :, 1:] = lab_image_np[:, :, 1:] * 255 - 127  # Scale A and B channels

        # Convert the LAB image to RGB using skimage's lab2rgb function
        rgb_image = lab2rgb(lab_image_np)

        # Plot the RGB image
        plt.figure(figsize=(6, 6))
        plt.imshow(rgb_image)
        plt.title(f'L = {l_value}')
        plt.axis('off')
        plt.show()
    
# def plot_predicted_image(model: torch.nn.Module, img: Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor], device: str = "cuda"):
#    """
#    Plot the predicted colorized image using the provided model and input tensors.

#    Args:
#        model (torch.nn.Module): The PyTorch model used for colorization.
#        img (Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]): A tuple containing the following tensors:
#            - RGB image tensor: Size([3, H, W])
#            - L channel tensor: Size([1, H, W])
#            - A channel tensor: Size([H, W])
#            - B channel tensor: Size([H, W])
#            - AB channels tensor: Size([2, H, W])
#        device (str, optional): The device to use for computations. Default is "cuda".
#    """
#    l_channel = img[1].to(device)
#    rgb = img[0].to(device)

#    with torch.no_grad():
#        ab_pred = model(l_channel)

#    plot_l(l_channel.detach().cpu())
#    plot_rgb(rgb.detach().cpu())
#    reconstruct_lab(l_channel.detach().cpu(), ab_pred.detach().cpu())

def reconstruct_lab(l_channel: torch.Tensor, ab_channels: Tuple[torch.Tensor, torch.Tensor]):
    """
    Reconstructs an RGB image from its L, A, and B channels.

    Args:
        l_channel (torch.Tensor): Tensor containing the L channel values. Size 1xHxW. Values in [0,1].
        ab_channels (Tuple[torch.Tensor, torch.Tensor]): Tuple containing the A and B channel tensors. Values in [0,1].
            A channel tensor: Size HxW.
            B channel tensor: Size HxW.
    """
    a_channel = ab_channels[0]
    b_channel = ab_channels[1]
    l_channel = l_channel.squeeze()  # from 1xHxW to HxW
    lab_image = torch.stack((l_channel, a_channel, b_channel), dim=0)

    # revert normalization of L channel
    l_channel_np = l_channel.cpu().numpy() * 100

    # revert normalization of A and B channels
    ab_channels_np = torch.stack((a_channel, b_channel), dim=0).permute(1, 2, 0).cpu().numpy() * 255 - 128

    # stack L, A, B channels
    lab_image_reconstructed = np.zeros((lab_image.shape[1], lab_image.shape[2], 3))
    lab_image_reconstructed[:, :, 0] = l_channel_np
    lab_image_reconstructed[:, :, 1:] = ab_channels_np

    # convert LAB image to RGB
    rgb_image = lab2rgb(lab_image_reconstructed)

    # display the RGB image
    plt.figure(figsize=(6, 6))
    plt.imshow(rgb_image)
    plt.axis('off')
    plt.show()
    
def plot_model_pred(l, model, device):
    input = l.to(device).unsqueeze(0)
    ab_pred = model(input).squeeze(0)
    reconstruct_lab(l, ab_pred.detach().cpu())