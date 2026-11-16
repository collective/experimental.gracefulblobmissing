from setuptools import setup


version = "3.0.dev0"

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
        "Framework :: Plone :: 6.2",
        'Framework :: Plone :: 5.1',
        'Framework :: Plone :: 5.2',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    keywords="plone blob patch",
    author="RedTurtle Technology",
    author_email="sviluppoplone@redturtle.it",
    url="http://plone.org/products/experimental.gracefulblobmissing",
    license="GPL",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "collective.monkeypatcher>=1.0",
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
