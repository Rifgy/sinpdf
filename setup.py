from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='sinpdf',
    version='0.1',
    license='MIT',
    author='Rifgy',
    author_email='z-ybr@mail.ru',
    keywords=['sqlite', 'pdf-viewer', 'pdf'],
    url='https://github.com/Rifgy/sinpdf.git',
    description='Small program for scan PDF files massive and fast search text in result.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    #packages=['sinpdf'],
    package_dir = {"": "sinpdf"},
    packages = find_packages(where="sinpdf"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'PyQt5>=5.15.11',
        'SQLAlchemy>=2.0.41',
        'pdfplumber>=0.11.6'
        ],
    python_requires = ">=3.6",
    entry_points={
        'console_scripts': ['sinpdf = sinpdf.main',]
    },
)