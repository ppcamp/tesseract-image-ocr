# Open image

from os import path, listdir
from cv2 import imread, cvtColor, medianBlur, threshold, dilate, erode, morphologyEx, Canny, minAreaRect, matchTemplate
import cv2
from pprint import pprint
import numpy as np
import pytesseract
from pytesseract import Output


# basis class
class Image:
    def __init__(self, path: str = None):
        self.__image = None
        if path:
            self.load(path)

    # load image
    def load(self, path: str):
        self.__image = imread(path)
        return self

    # get image
    def get(self):
        return self.__image

    # convert the image object to gray
    def to_gray(self):
        self.__image = cvtColor(self.__image, cv2.COLOR_BGR2GRAY)
        return self

    # noise removal
    def remove_noise(self):
        return medianBlur(self.__image, 5)

    # thresholding
    def thresholding(self):
        return threshold(self.__image, 0, 255,
                         cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # dilation
    def dilate(self):
        kernel = np.ones((5, 5), np.uint8)
        return dilate(self.__image, kernel, iterations=1)

    # erosion
    def erode(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return erode(image, kernel, iterations=1)

    # opening - erosion followed by dilation
    def opening(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return morphologyEx(image, cv2.MORPH_OPEN, kernel)

    # canny edge detection
    def canny(self, image):
        return Canny(image, 100, 200)

    # skew correction
    def deskew(self, image):
        coords = np.column_stack(np.where(image > 0))
        angle = minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    # template matching
    def match_template(self, image, template):
        return matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


# Main method
def main():
    # Get path to this file
    currdir = path.dirname(path.realpath(__file__))

    # configure assets folder location
    assets_folder = path.join(currdir, '..', '..', 'assets')

    # list all elements in this folder
    assets_files = listdir(assets_folder)

    # filter to get only anime_ prefix
    anime_images = list(
        filter(lambda image: 'anime' in image, assets_files))
    anime_images = sorted(anime_images)

    # create a list of images based on this items
    images = list(map(lambda image: Image(
        path.join(assets_folder, image)), assets_files))

    # print all images
    for image in images:
        cv2.imshow(f'ANIME_IMAGES', image.get())

        # convert the image to data
        data = pytesseract.image_to_data(image.get(), output_type=Output.DICT)
        keys = list(data.keys())
        pprint(keys)
        pprint(f'Data: {data}')

        # wait until type some key
        cv2.waitKey()

    # Call this method
if __name__ == '__main__':
    main()
