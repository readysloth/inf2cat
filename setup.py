from setuptools import setup


setup(name='inf2cat',
      version='0.1',
      packages=['inf2cat'],
      description='Creates .cat file without even using .inf',
      build_with_nuitka=True,
      entry_points={
          'console_scripts': ['inf2cat = inf2cat:main'],
      },
      install_requires=[
          'cffi==1.15.1',
          'cryptography==40.0.2',
          'pycparser==2.21',
          'asn1crypto==1.5.1'
      ])
