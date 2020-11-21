from setuptools import setup, find_packages

setup(
    name="xps.browserhist",
    verison="0.1.0",
    author="Ashoka Lella",
    py_modules=find_packages(),
    install_requires=[
        "elasticsearch",
        "python-dateutil",
        "tqdm",
    ],
    entry_points="""
        [console_scripts]
        browserhist=cli:cli
    """,
) 