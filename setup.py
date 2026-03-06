import setuptools

setuptools.setup(
    name="cap-demo-image-processing",
    version="0.0.1",
    author="DigiNova",
    author_email='info@diginova.com.tr',
    description="Demo image processing package with grayscale conversion and edge detection.",
    url='https://github.com/novavision-ai/cap-demo-image-processing',
    license='MIT',
    install_requires=['sdk', 'opencv-python-headless', 'numpy'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=[
        'novavision.cap_demo_image_processing',
        'novavision.cap_demo_image_processing.executors',
        'novavision.cap_demo_image_processing.models',
        'novavision.cap_demo_image_processing.utils',
    ],
    package_dir={'novavision.cap_demo_image_processing': 'src'},
    python_requires=">=3.6"
)