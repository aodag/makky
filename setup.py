from setuptools import setup, find_packages

requires = [
    "webob",
    "mako",
    "beaker",
    "cliff",
]

tests_require = [
    "pytest",
    "pytest-cov",
    "webtest",
]

setup(name="makky",
      version="0.0",
      install_requires=requires,
      tests_require=tests_require,
      extras_require={
          "testing": tests_require,
      },
      packages=find_packages('src'),
      package_dir={"": "src"},
)
