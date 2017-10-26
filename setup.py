
from setuptools import setup

setup(
    name='fttl',
    version='0.1.0',
    author='Assi Maimon',
    author_email='maimon33@gmail.com',
    license='LICENSE',
    py_modules=['fttl'],
    description='Self destruct for files',
    entry_points={
        'console_scripts': [
                'fttl=fttl:fttl',
        ],
    },
    install_requires=[
        'click==6.6',
        'click-didyoumean==0.0.3',
        'psutil==5.4.0',
    ]
)
