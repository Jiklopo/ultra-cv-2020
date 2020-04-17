import cv2
import numpy as np
import os

class ImageProcessor:
    def __init__(self, image_path):
        self.file = image_path
        self.img = cv2.imread(self.file)
        self.height, self.width = np.shape(self.img)[:2]
        self.aspect_ratio = self.width / self.height

    def find_object(self):
        img = cv2.imread(self.blur())
        img2 = cv2.imread(self.file)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 10, 200, apertureSize=3)

        contours, _ = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        target = np.argmax([cv2.arcLength(cnt, True) for cnt in contours])

        try:
            (x, y), radius = cv2.minEnclosingCircle(contours[target])
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(img2, center, radius, (0, 255, 0), 3)

            c = cv2.approxPolyDP(contours[target], 0.009, True)
            cv2.drawContours(img2, [c], 0, (0, 0, 255), 3)
        finally:
            cv2.imwrite('results/img.png', img2)
            return os.path.abspath('results/img.png')

    def blur(self):
        k_size = ((self.width + self.height) // 200) * 2 + 1
        img = cv2.GaussianBlur(self.img, (k_size, k_size), 1.2)

        cv2.imwrite('results/blur.png', img)
        return os.path.abspath('results/blur.png')

    def gray(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('results/gray.png', gray)
        return os.path.abspath('results/gray.png')

    def threshold(self):
        img = cv2.imread(self.blur())
        th = cv2.adaptiveThreshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 5)
        cv2.imwrite('results/th.png', th)
        return os.path.abspath('results/th.png')

    def edges(self):
        img = cv2.imread(self.blur())
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 10, 200, apertureSize=3)
        cv2.imwrite('results/edge.png', edge)
        return os.path.abspath('results/edge.png')

