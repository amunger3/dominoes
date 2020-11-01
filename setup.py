from setuptools import setup

setup(
    name='dominoes',
    version='1.0.0',
    description='A Python library for the game of dominoes, with an accompanying CLI and AI players.',
    url='https://github.com/amunger3/dominoes',
    author='Alan Wagner',
    author_email='munger.alex@gmail.com',
    license='MIT',
    packages=['dominoes'],
    scripts=['bin/dominoes'],
    test_suite='tests'
)
