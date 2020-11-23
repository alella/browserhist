from setuptools import setup, find_packages

setup(
    name="xps.browserhist",
    version="0.3.1",
    author="Ashoka Lella",
    py_modules=find_packages(),
    install_requires=[
        "elasticsearch",
        "python-dateutil",
        "click",
        "coloredlogs"
    ],
    entry_points="""
        [console_scripts]
        browserhist=xps.browserhist:cli
    """,
)
