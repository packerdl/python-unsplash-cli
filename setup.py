from setuptools import setup

setup(
    name='unsplash-cli',
    version='0.0.0',
    description='',
    author='Devin Packer',
    license='MIT',
    packages=['unsplash'],
    zip_safe=False,
    install_requires=[
        'click',
        'halo',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        unsplash=unsplash.__main__:main
    '''
)
