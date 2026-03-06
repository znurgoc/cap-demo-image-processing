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
# dependentDropdown: ConversionMode
#   Option 1 (ConversionModeCustom)  → textInput  (Red channel weight)
#   Option 2 (ConversionModePreset)  → dropdownlist (Preset method)
# =============================================================================

# --- Option 1: Custom Weight → textInput ---

class GrayWeightR(Config):
    name: Literal["GrayWeightR"] = "GrayWeightR"
    value: float = Field(ge=0.0, le=1.0, default=0.299)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0.0, 1.0]"] = "[0.0, 1.0]"

    class Config:
        title = "Red Channel Weight"


class ConversionModeCustom(Config):
    name: Literal["ConversionModeCustom"] = "ConversionModeCustom"
    grayWeightR: GrayWeightR
    value: Literal["ConversionModeCustom"] = "ConversionModeCustom"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Custom Weights"


# --- Option 2: Preset Method → dropdownlist ---

class PresetLuminosity(Config):
    name: Literal["Luminosity"] = "Luminosity"
    value: Literal["Luminosity"] = "Luminosity"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Luminosity"


class PresetAverage(Config):
    name: Literal["Average"] = "Average"
    value: Literal["Average"] = "Average"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Average"


class PresetLightness(Config):
    name: Literal["Lightness"] = "Lightness"
    value: Literal["Lightness"] = "Lightness"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Lightness"


class ConversionPreset(Config):
    name: Literal["ConversionPreset"] = "ConversionPreset"
    value: Union[PresetLuminosity, PresetAverage, PresetLightness]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Preset Method"


class ConversionModePreset(Config):
    name: Literal["ConversionModePreset"] = "ConversionModePreset"
    conversionPreset: ConversionPreset
    value: Literal["ConversionModePreset"] = "ConversionModePreset"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Preset Method"


# --- dependentDropdown ---

class ConversionMode(Config):
    name: Literal["ConversionMode"] = "ConversionMode"
    value: Union[ConversionModeCustom, ConversionModePreset]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Conversion Mode"


# --- Grayscale Configs / Inputs / Outputs ---

class GrayscaleInputs(Inputs):
    inputImage: InputImage


class GrayscaleConfigs(Configs):
    conversionMode: ConversionMode


class GrayscaleOutputs(Outputs):
    outputImage: OutputImage


# --- Request & Response ---

class GrayscaleRequest(Request):
    inputs: Optional[GrayscaleInputs]
    configs: GrayscaleConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class GrayscaleResponse(Response):
    outputs: GrayscaleOutputs


# --- Executor ---

class GrayscaleExecutor(Config):
    name: Literal["GrayscaleExecutor"] = "GrayscaleExecutor"
    value: Union[GrayscaleRequest, GrayscaleResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Grayscale Conversion"
        json_schema_extra = {"target": {"value": 0}}


# =============================================================================
# EXECUTOR 2 — EdgeDetectionExecutor
# 2 inputs:  inputImage + inputMaskImage
# 2 outputs: outputEdgeImage + outputStatImage
# dependentDropdown: DetectionMode
#   Option 1 (DetectionModeCanny) → textInput    (Canny threshold)
#   Option 2 (DetectionModeSobel) → dropdownlist (Sobel kernel size)
# =============================================================================

# --- Option 1: Canny → textInput ---

class CannyThresholdLow(Config):
    name: Literal["CannyThresholdLow"] = "CannyThresholdLow"
    value: float = Field(ge=0.0, le=255.0, default=50.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0, 255]"] = "[0, 255]"

    class Config:
        title = "Canny Low Threshold"


class DetectionModeCanny(Config):
    name: Literal["DetectionModeCanny"] = "DetectionModeCanny"
    cannyThresholdLow: CannyThresholdLow
    value: Literal["DetectionModeCanny"] = "DetectionModeCanny"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Canny"


# --- Option 2: Sobel → dropdownlist ---

class SobelKernel3(Config):
    name: Literal["SobelKernel3"] = "SobelKernel3"
    value: Literal["3"] = "3"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Kernel 3x3"


class SobelKernel5(Config):
    name: Literal["SobelKernel5"] = "SobelKernel5"
    value: Literal["5"] = "5"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Kernel 5x5"


class SobelKernel7(Config):
    name: Literal["SobelKernel7"] = "SobelKernel7"
    value: Literal["7"] = "7"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Kernel 7x7"


class SobelKernelSize(Config):
    name: Literal["SobelKernelSize"] = "SobelKernelSize"
    value: Union[SobelKernel3, SobelKernel5, SobelKernel7]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Sobel Kernel Size"


class DetectionModeSobel(Config):
    name: Literal["DetectionModeSobel"] = "DetectionModeSobel"
    sobelKernelSize: SobelKernelSize
    value: Literal["DetectionModeSobel"] = "DetectionModeSobel"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Sobel"


# --- dependentDropdown ---

class DetectionMode(Config):
    name: Literal["DetectionMode"] = "DetectionMode"
    value: Union[DetectionModeCanny, DetectionModeSobel]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Detection Mode"


# --- Edge Detection Configs / Inputs / Outputs ---

class EdgeDetectionInputs(Inputs):
    inputImage: InputImage
    inputMaskImage: InputMaskImage


class EdgeDetectionConfigs(Configs):
    detectionMode: DetectionMode


class EdgeDetectionOutputs(Outputs):
    outputEdgeImage: OutputEdgeImage
    outputStatImage: OutputStatImage


# --- Request & Response ---

class EdgeDetectionRequest(Request):
    inputs: Optional[EdgeDetectionInputs]
    configs: EdgeDetectionConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class EdgeDetectionResponse(Response):
    outputs: EdgeDetectionOutputs


# --- Executor ---

class EdgeDetectionExecutor(Config):
    name: Literal["EdgeDetectionExecutor"] = "EdgeDetectionExecutor"
    value: Union[EdgeDetectionRequest, EdgeDetectionResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Edge Detection"
        json_schema_extra = {"target": {"value": 0}}


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
    uID = "9900001"