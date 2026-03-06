from sdks.novavision.src.helper.package import PackageHelper
from components.cap_demo_image_processing.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor,
    GrayscaleExecutor, GrayscaleResponse, GrayscaleOutputs, OutputImage,
    EdgeDetectionExecutor, EdgeDetectionResponse, EdgeDetectionOutputs, OutputEdgeImage, OutputStatImage
)


def build_grayscale_response(context):
    outputImage = OutputImage(value=context.image)
    outputs = GrayscaleOutputs(outputImage=outputImage)
    packageResponse = GrayscaleResponse(outputs=outputs)
    packageExecutor = GrayscaleExecutor(value=packageResponse)
    executor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_edge_detection_response(context):
    outputEdgeImage = OutputEdgeImage(value=context.edge_image)
    outputStatImage = OutputStatImage(value=context.stat_image)
    outputs = EdgeDetectionOutputs(outputEdgeImage=outputEdgeImage, outputStatImage=outputStatImage)
    packageResponse = EdgeDetectionResponse(outputs=outputs)
    packageExecutor = EdgeDetectionExecutor(value=packageResponse)
    executor = ConfigExecutor(value=packageExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
