from setuptools import setup, find_packages
import os

version = '0.3.0'

setup(name='experimental.gracefulblobmissing',
      version=version,
      description="Patch for Plone. Not raise error when visiting file contents with missing BLOB file",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        ],
      keywords='plone blob patch',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.net',
      url='http://svn.plone.org/svn/collective/experimental.gracefulblobmissing/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['experimental'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.monkeypatcher>=1.0',
          'plone.app.blob',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
