from setuptools import setup, find_packages

setup(
    name="xps.browserhist",
    version="0.3.5",
    author="Ashoka Lella",
    packages=find_packages(),
    install_requires=[
        "elasticsearch",
        "python-dateutil",
        "click",
        "coloredlogs"
    ],
    entry_points={
        'console_scripts': ['browserhist = xps.browserhist.cli:cli']
    }
)
