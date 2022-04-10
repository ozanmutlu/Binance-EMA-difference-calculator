
import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name='binance_ema_difference',
    version='1.0',
    packages=setuptools.find_packages(),
    install_requires=required,
    console=['__main__.py']
)
