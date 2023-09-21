from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in green/__init__.py
from green import __version__ as version

setup(
	name="green",
	version=version,
	description="Custom App for customization in Greentek",
	author="kushdhallod@gmail.com",
	author_email="kushdhallod@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
