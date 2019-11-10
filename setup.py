from setuptools import find_packages, setup

setup(
    include_package_data=True,
    name='igloo',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    version='0.0.1',
    zip_safe=False,
)
