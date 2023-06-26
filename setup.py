from setuptools import setup, find_packages

setup(name='linkaform_api',
    version='3.0',
    description='LinkaForm API This API si created to use in python the services of the Linkaform API',
    url='https://github.com/linkaform/linkaform_api',
    author='Linkaform',
    author_email='develop@linkaform.com',
    license='GNU',
    packages=find_packages(),
    # packages=['linkaform_api', 'linkaform_api.models'],
    install_requires=[
        'pymongo',
        'pyexcel',
        'simplejson',
        'wget',
        'facturapi',
        'jinja2'
    ],
    zip_safe=False)
