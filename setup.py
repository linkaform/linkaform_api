from setuptools import setup

setup(name='linkaform_api',
    version='3.0',
    description='LinkaForm API This API si created to use in python the services of the Linkaform API',
    url='https://github.com/linkaform/linkaform_api',
    author='Linkaform',
    author_email='develop@linkaform.com',
    license='GNU',
    packages=['linkaform_api'],
    install_requires=[
        'futures',
        'pymongo',
        'pyexcel',
        'simplejson',
        'wget',
    ],
    zip_safe=False)
