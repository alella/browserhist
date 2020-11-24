from setuptools import setup, find_packages

setup(
    name="browserhist",
    version="0.4.0",
    author="Ashoka Lella",
    packages=find_packages(),
    install_requires=[
        "elasticsearch",
        "python-dateutil",
        "click",
        "coloredlogs"
    ],
    entry_points={
        'console_scripts': ['browserhist = browserhist.cli:cli']
    }
)
