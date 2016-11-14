from setuptools import setup

setup(
    name='ads-resolver',
    version='0.1',
    url='http://github.com/tymrl/ads-resolver',
    description='',
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'flask',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'ads-resolver = app:run',
        ]
    },
)
