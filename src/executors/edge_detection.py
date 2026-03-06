"""
    Edge Detection Executor — detects edges in an input image.
    Accepts two inputs:
        - inputImage     : main image to process
        - inputMaskImage : mask image (applied before edge detection)
    Produces two outputs:
        - outputEdgeImage : image showing detected edges
        - outputStatImage : image showing edge statistics overlay
    Supports two modes via dependentDropdown:
        - Canny : user provides low threshold value
        - Sobel : user selects kernel size (3x3, 5x5, 7x7)
"""

import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.capsule import Capsule
from components.cap_demo_image_processing.src.models.PackageModel import PackageModel
from components.cap_demo_image_processing.src.utils.response import build_edge_detection_response


class EdgeDetectionExecutor(Capsule):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image = self.request.get_param("inputImage")
        self.mask_image = self.request.get_param("inputMaskImage")
        self.detection_mode = self.request.get_param("DetectionMode")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def apply_mask(self, image, mask):
        """
        Applies mask image to the main image.
        Only pixels where mask is non-zero are kept.
        """
        if mask is None:
            return image
        mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        _, mask_binary = cv2.threshold(mask_gray, 1, 255, cv2.THRESH_BINARY)
        return cv2.bitwise_and(image, image, mask=mask_binary)

    def detect_edges(self, image):
        """
        Detects edges based on selected detection mode.
        DetectionModeCanny → uses user-defined low threshold
        DetectionModeSobel → uses user-selected kernel size
        """
        mode_name = self.detection_mode.get("name")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if mode_name == "DetectionModeCanny":
            # Canny edge detection with user-defined low threshold
            low_threshold = float(
                self.detection_mode.get("cannyThresholdLow", {}).get("value", 50.0)
            )
            high_threshold = low_threshold * 2
            edges = cv2.Canny(gray, low_threshold, high_threshold)

        elif mode_name == "DetectionModeSobel":
            # Sobel edge detection with user-selected kernel size
            kernel_value = self.detection_mode.get("sobelKernelSize", {}).get("value", "3")
            ksize = int(kernel_value)
            sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
            sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
            edges = cv2.magnitude(sobel_x, sobel_y)
            edges = np.clip(edges, 0, 255).astype(np.uint8)

        else:
            edges = cv2.Canny(gray, 50, 100)

        # Convert to 3-channel for consistent output format
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def build_stat_image(self, original, edges):
        """
        Creates a statistics overlay image.
        Shows edge pixels highlighted in green on the original image.
        """
        stat_image = original.copy()
        edge_gray = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
        stat_image[edge_gray > 0] = [0, 255, 0]
        edge_count = int(np.count_nonzero(edge_gray))
        total_pixels = edge_gray.size
        edge_ratio = round((edge_count / total_pixels) * 100, 2)
        cv2.putText(
            stat_image,
            f"Edges: {edge_count} px ({edge_ratio}%)",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
        return stat_image

    def run(self):
        # Load main image
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)

        # Load mask image
        mask = Image.get_frame(img=self.mask_image, redis_db=self.redis_db)

        # Apply mask to main image
        masked = self.apply_mask(img.value, mask.value)

        # Detect edges
        edges = self.detect_edges(masked)

        # Build stat image
        stat = self.build_stat_image(img.value, edges)

        # Save outputs
        img.value = edges
        self.edge_image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)

        mask.value = stat
        self.stat_image = Image.set_frame(img=mask, package_uID=self.uID, redis_db=self.redis_db)

        packageModel = build_edge_detection_response(context=self)
        return packageModel