from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='pyramid_mongo',
      version=version,
      description="Mongodb support for pyramid",
      long_description="""\
        This plugin lets you create a connection to a mongodb server and query its database.
        It currently only support one database, one host and authentication
""",
      classifiers=[],
      keywords='pymongo mongodb pyramid',
      author='Lo\xc3\xafc Faure-Lacroix',
      author_email='lamerstar@gmail.com',
      url='delicieuxgateau.ca',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'pyramid',
          'pymongo',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
