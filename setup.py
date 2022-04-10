
from distutils.core import setup
import py2exe
import setuptools
from distutils.core import setup
with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name='binance_ema_difference',
    version='1.0',
    packages=setuptools.find_packages(),
    install_requires=required,
    console=['__main__.py'],
    options = {'py2exe': {
        "optimize": 2,
        "bundle_files": 2, # This tells py2exe to bundle everything
      }},
)
