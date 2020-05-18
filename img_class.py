from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

class image:
    def __init__(self,path):
            self.img =cv2.imread(path,0) 
            # load the image data into a numpy array
            #self.img_data = np.asarray(self.img)
            # perform the 2-D fast Fourier transform on the image data
            self.fourier = np.fft.fft2(self.img)
            # move the zero-frequency component to the center of the Fourier spectrum
            #self.fourier_shift = np.fft.fftshift(self.fourier)
            #phase computation
            self.phase_spectrum = np.angle(self.fourier)
            #real part
            self.real_spectrum = np.real(self.fourier)
            #imag part 
            self.imag_spectrum = np.imag(self.fourier)
            # compute the magnitudes (absolute values) of the complex numbers
            self.fourier_abs = np.abs(self.fourier)
            # compute the common logarithm of each value to reduce the dynamic range
            self.mag_spectrum = np.log10(self.fourier_abs)
            #uniform magnitude
            self.uniform_mag = np.where(self.mag_spectrum, 1, self.mag_spectrum)
            #uniform phase
            self.uniform_phase = np.where(self.phase_spectrum, 0, self.phase_spectrum)
            self.shape= self.img.shape


            








""" 
# open an 8bpp indexed image
img = cv2.imread('test3.jpeg',0)
img2 = cv2.imread('test4.jpeg',0)
if(img.shape == img2.shape):
    print('true')
else:
    print('false')
# load the image data into a numpy array
img_data = np.asarray(img)
# perform the 2-D fast Fourier transform on the image data
fourier = np.fft.fft2(img_data)
# move the zero-frequency component to the center of the Fourier spectrum
fourier_shift = np.fft.fftshift(fourier)
#phase computation
phase_spectrum = np.angle(fourier_shift)
#real part
real_spectrum = np.real(fourier_shift)
#imag part 
imag_spectrum = np.imag(fourier_shift)
# compute the magnitudes (absolute values) of the complex numbers
fourier = np.abs(fourier_shift)
# compute the common logarithm of each value to reduce the dynamic range
fourier = np.log10(fourier)
"""

# show the normalized Fourier image
#norm_fourier_img.show()

# convert the output image to 8-bit pixels (grayscale) and save it
#norm_fourier_img.convert('L').save('test.bmp')