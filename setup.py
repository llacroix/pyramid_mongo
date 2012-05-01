from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='pyramid_mongo',
      version=version,
      description="A simple package to handle mongodb in pyramid",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Lo\xc3\xafc Faure-Lacroix',
      author_email='lamerstar@gmail.com',
      url='delicieuxgateau.ca',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
