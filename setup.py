from setuptools import setup, find_packages

version = '0.1'

testing_extras = ['nose', 'coverage']
docs_extras = ['Sphinx']

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
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite="pyramid_mongo",
      install_requires=[
          # -*- Extra requirements: -*-
          'pyramid',
          'pymongo',
      ],
      extras_require = {
          'dev':testing_extras,
          'docs':docs_extras,
          },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
