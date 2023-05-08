from setuptools import find_packages, setup

NAME = "access"

# This will load the version from the version.py file
__version__ = "1.0"
exec(open('src/%s/version.py' % NAME).read())

with open("requirements.txt", "r") as rq:
    packages_list = rq.read()

setup(
    name=NAME,
    version=__version__,
    author="Shashank Khandelwal",
    author_email="s2k2dk@yahoo.com",
    include_package_data=True,
    install_requires=[
        packages_list,
    ],

    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    )

)
