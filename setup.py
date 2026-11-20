from setuptools import setup

version = "3.0.dev0"

setup(
    name="experimental.gracefulblobmissing",
    version=version,
    description=(
        "Patch for Plone. "
        "Don't raise errors for file contents with missing BLOB file"
    ),
    long_description=open("README.md").read() + "\n" + open("CHANGES.md").read(),
    long_description_content_type="text/markdown",
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: 6.3",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.15",
    ],
    keywords="plone blob patch",
    author="RedTurtle Technology",
    author_email="sviluppoplone@redturtle.it",
    project_urls={
        "Homepage": "https://github.com/collective/experimental.gracefulblobmissing"
    },
    license_expression="GPL-2.0-or-later",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.11",
    install_requires=[
        "collective.monkeypatcher>=1.0",
        "ZODB",
    ],
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
