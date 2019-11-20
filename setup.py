from setuptools import setup


requirements = [
    'setuptools',
    'Django'        
]

setup(
    name='django-coreuikit',
    packages=['coreuikit'],
    version='0.1',
    license='GPL',
    long_description=open('README.rst').read(),
    url='https://github.com/iomarmochtar/django-coreuikit',
    author='Imam Omar Mochtar',
    author_email='iomarmochtar@gmail.com',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
    ],
    install_requires=requirements
)
