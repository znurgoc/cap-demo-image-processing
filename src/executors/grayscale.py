"""
    Grayscale Executor — converts an input image to grayscale.
    Supports two modes via dependentDropdown:
        - Custom Weights : user provides red channel weight
        - Preset Method  : Luminosity / Average / Lightness
"""

import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.capsule import Capsule
from components.cap_demo_image_processing.src.models.PackageModel import PackageModel
from components.cap_demo_image_processing.src.utils.response import build_grayscale_response


class GrayscaleExecutor(Capsule):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image = self.request.get_param("inputImage")
        self.conversion_mode = self.request.get_param("ConversionMode")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def convert_to_grayscale(self, image):
        """
        Converts image to grayscale based on selected conversion mode.
        ConversionModeCustom  → uses user-defined red channel weight
        ConversionModePreset  → uses a standard preset method
        """
        mode_name = self.conversion_mode.get("name")

        if mode_name == "ConversionModeCustom":
            # Custom weight: user provides red channel weight (0.0 - 1.0)
            weight_r = float(self.conversion_mode.get("grayWeightR", {}).get("value", 0.299))
            # Remaining weight split equally between green and blue
            weight_g = round((1.0 - weight_r) * 0.587 / (0.587 + 0.114), 4)
            weight_b = round(1.0 - weight_r - weight_g, 4)
            gray = cv2.transform(image, np.array([[weight_b, weight_g, weight_r]]))

        elif mode_name == "ConversionModePreset":
            preset = self.conversion_mode.get("conversionPreset", {}).get("value", "Luminosity")

            if preset == "Luminosity":
                # Standard luminosity weights (ITU-R BT.601)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            elif preset == "Average":
                # Simple average of all channels
                gray = np.mean(image, axis=2).astype(np.uint8)

            elif preset == "Lightness":
                # Lightness: average of max and min channel values
                gray = ((image.max(axis=2).astype(np.uint16) +
                         image.min(axis=2).astype(np.uint16)) // 2).astype(np.uint8)
            else:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Convert back to 3-channel so output format is consistent
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.convert_to_grayscale(img.value)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_grayscale_response(context=self)
        return packageModel