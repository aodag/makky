import os
from setuptools import setup, find_packages

here = os.path.dirname(__file__)

requires = [
    "webob",
    "mako",
    "beaker",
    "cliff",
    "gearbox",
    "gunicorn",
    "backlash",
]

tests_require = [
    "pytest",
    "pytest-cov",
    "webtest",
]

readme = open(os.path.join(here, "README.rst")).read()

points = {
    "paste.app_factory": [
        "main=makky:main",
    ],
}

setup(name="makky",
      version="0.0",
      long_description=readme,
      install_requires=requires,
      tests_require=tests_require,
      extras_require={
          "testing": tests_require,
      },
      packages=find_packages('src'),
      package_dir={"": "src"},
      entry_points=points,
)
