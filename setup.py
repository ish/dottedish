from setuptools import setup, find_packages
import sys, os

version = '0.5'

setup(name='dottedish',
      version=version,
      description="A dotted key accessor that handles numeric keys for list entries",
      long_description="""\
""",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2",
      ], 
      keywords='dictionary dict dotted deep',
      author='Tim Parkin, Matt Goodall',
      author_email='developers@ish.io',
      url='http://ish.io/projects/show/dottedish',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          "WebOb",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite="dottedish.tests"
      )
