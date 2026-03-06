from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


# =============================================================================
# INPUTS
# =============================================================================

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class InputMaskImage(Input):
    name: Literal["inputMaskImage"] = "inputMaskImage"
    value: Optional[Union[List[Image], Image]] = None
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Mask Image"


# =============================================================================
# OUTPUTS
# =============================================================================

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputEdgeImage(Output):
    name: Literal["outputEdgeImage"] = "outputEdgeImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Edge Image"


class OutputStatImage(Output):
    name: Literal["outputStatImage"] = "outputStatImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Stat Image"


# =============================================================================
# EXECUTOR 1 — GrayscaleExecutor
# dependentDropdown: conversionMode
#   Option 1 (conversionModeCustom)  → textInput  (Red channel weight)
#   Option 2 (conversionModePreset)  → dropdownlist (Preset method)
# =============================================================================

class GrayWeightR(Config):
    name: Literal["grayWeightR"] = "grayWeightR"
    value: float = Field(ge=0.0, le=1.0, default=0.299)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0.0, 1.0]"] = "[0.0, 1.0]"

    class Config:
        title = "Red Channel Weight"
        json_schema_extra = {
            "shortDescription": "Weight of the red channel in grayscale conversion (0.0 - 1.0)"
        }


class ConversionModeCustom(Config):
    name: Literal["conversionModeCustom"] = "conversionModeCustom"
    grayWeightR: GrayWeightR
    value: Literal["conversionModeCustom"] = "conversionModeCustom"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Custom Weights"
        json_schema_extra = {
            "shortDescription": "Define custom red channel weight for grayscale conversion"
        }


class PresetLuminosity(Config):
    name: Literal["luminosity"] = "luminosity"
    value: Literal["luminosity"] = "luminosity"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Luminosity"
        json_schema_extra = {
            "shortDescription": "Standard ITU-R BT.601 luminosity weights"
        }


class PresetAverage(Config):
    name: Literal["average"] = "average"
    value: Literal["average"] = "average"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Average"
        json_schema_extra = {
            "shortDescription": "Simple average of all RGB channels"
        }


class PresetLightness(Config):
    name: Literal["lightness"] = "lightness"
    value: Literal["lightness"] = "lightness"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Lightness"
        json_schema_extra = {
            "shortDescription": "Average of max and min channel values"
        }


class ConversionPreset(Config):
    name: Literal["conversionPreset"] = "conversionPreset"
    value: Union[PresetLuminosity, PresetAverage, PresetLightness]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Preset Method"
        json_schema_extra = {
            "shortDescription": "Select a standard grayscale conversion method"
        }


class ConversionModePreset(Config):
    name: Literal["conversionModePreset"] = "conversionModePreset"
    conversionPreset: ConversionPreset
    value: Literal["conversionModePreset"] = "conversionModePreset"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Preset Method"
        json_schema_extra = {
            "shortDescription": "Use a preset grayscale conversion method"
        }


class ConversionMode(Config):
    name: Literal["conversionMode"] = "conversionMode"
    value: Union[ConversionModeCustom, ConversionModePreset]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Conversion Mode"
        json_schema_extra = {
            "shortDescription": "Choose between custom weights or a preset grayscale method"
        }


class GrayscaleInputs(Inputs):
    inputImage: InputImage


class GrayscaleConfigs(Configs):
    conversionMode: ConversionMode


class GrayscaleOutputs(Outputs):
    outputImage: OutputImage


class GrayscaleRequest(Request):
    inputs: Optional[GrayscaleInputs]
    configs: GrayscaleConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class GrayscaleResponse(Response):
    outputs: GrayscaleOutputs


# FIX: Executor name değeri class ismiyle birebir aynı (PascalCase)
class GrayscaleExecutor(Config):
    name: Literal["GrayscaleExecutor"] = "GrayscaleExecutor"
    value: Union[GrayscaleRequest, GrayscaleResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Grayscale Conversion"
        json_schema_extra = {
            "target": {"value": 0},
            "shortDescription": "Convert input image to grayscale"
        }


# =============================================================================

# =============================================================================

class CannyThresholdLow(Config):
    name: Literal["cannyThresholdLow"] = "cannyThresholdLow"
    value: float = Field(ge=0.0, le=255.0, default=50.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0, 255]"] = "[0, 255]"

    class Config:
        title = "Canny Low Threshold"
        json_schema_extra = {
            "shortDescription": "Lower threshold for Canny edge detection (0 - 255)"
        }


class DetectionModeCanny(Config):
    name: Literal["detectionModeCanny"] = "detectionModeCanny"
    cannyThresholdLow: CannyThresholdLow
    value: Literal["detectionModeCanny"] = "detectionModeCanny"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Canny"
        json_schema_extra = {
            "shortDescription": "Detect edges using Canny algorithm with custom threshold"
        }


class SobelKernel3(Config):
    name: Literal["sobelKernel3"] = "sobelKernel3"
    value: Literal["3"] = "3"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Kernel 3x3"
        json_schema_extra = {
            "shortDescription": "Use 3x3 kernel for Sobel edge detection"
        }


class SobelKernel5(Config):
    name: Literal["sobelKernel5"] = "sobelKernel5"
    value: Literal["5"] = "5"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Kernel 5x5"
        json_schema_extra = {
            "shortDescription": "Use 5x5 kernel for Sobel edge detection"
        }


class SobelKernel7(Config):
    name: Literal["sobelKernel7"] = "sobelKernel7"
    value: Literal["7"] = "7"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Kernel 7x7"
        json_schema_extra = {
            "shortDescription": "Use 7x7 kernel for Sobel edge detection"
        }


class SobelKernelSize(Config):
    name: Literal["sobelKernelSize"] = "sobelKernelSize"
    value: Union[SobelKernel3, SobelKernel5, SobelKernel7]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Sobel Kernel Size"
        json_schema_extra = {
            "shortDescription": "Select kernel size for Sobel edge detection"
        }


class DetectionModeSobel(Config):
    name: Literal["detectionModeSobel"] = "detectionModeSobel"
    sobelKernelSize: SobelKernelSize
    value: Literal["detectionModeSobel"] = "detectionModeSobel"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Sobel"
        json_schema_extra = {
            "shortDescription": "Detect edges using Sobel algorithm with selected kernel size"
        }


class DetectionMode(Config):
    name: Literal["detectionMode"] = "detectionMode"
    value: Union[DetectionModeCanny, DetectionModeSobel]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Detection Mode"
        json_schema_extra = {
            "shortDescription": "Choose between Canny or Sobel edge detection algorithm"
        }


class EdgeDetectionInputs(Inputs):
    inputImage: InputImage
    inputMaskImage: Optional[InputMaskImage] = None  # FIX: Optional — Pydantic won't crash if not provided


class EdgeDetectionConfigs(Configs):
    detectionMode: DetectionMode


class EdgeDetectionOutputs(Outputs):
    outputEdgeImage: OutputEdgeImage
    outputStatImage: OutputStatImage


class EdgeDetectionRequest(Request):
    inputs: Optional[EdgeDetectionInputs]
    configs: EdgeDetectionConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class EdgeDetectionResponse(Response):
    outputs: EdgeDetectionOutputs


class EdgeDetectionExecutor(Config):
    name: Literal["EdgeDetectionExecutor"] = "EdgeDetectionExecutor"
    value: Union[EdgeDetectionRequest, EdgeDetectionResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Edge Detection"
        json_schema_extra = {
            "target": {"value": 0},
            "shortDescription": "Detect edges in image using Canny or Sobel algorithm"
        }


# =============================================================================
# PACKAGE LEVEL
# =============================================================================


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[GrayscaleExecutor, EdgeDetectionExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["capsule"] = "capsule"
    name: Literal["DemoImageProcessing"] = "DemoImageProcessing"
    uID: str = "9900001"