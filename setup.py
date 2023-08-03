from setuptools import find_packages
from setuptools import setup


version = "2.0"

setup(
    name="experimental.gracefulblobmissing",
    version=version,
    description=(
        "Patch for Plone. "
        "Don't raise errors for file contents with missing BLOB file"
    ),
    long_description=open("README.rst").read()
    + "\n"
    + open("CHANGES.rst").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        'Framework :: Plone :: 5.1',
        'Framework :: Plone :: 5.2',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords="plone blob patch",
    author="RedTurtle Technology",
    author_email="sviluppoplone@redturtle.it",
    url="http://plone.org/products/experimental.gracefulblobmissing",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["experimental"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "collective.monkeypatcher>=1.0",
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
