import setuptools

def _requires_from_file(filename):
    return open(filename).read().splitlines()
 
setuptools.setup(
    name="koui",
    version="1.0",
    author="nakamura196",
    author_email="na.kamura.1263@gmail.com",
    description="テキスト間の校異情報を扱うライプラリです。",
    long_description="テキスト間の校異情報を扱うライプラリです。",
    long_description_content_type="text/markdown",
    url="https://github.com/ldasjp8/koui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=_requires_from_file('requirements.txt'),
)