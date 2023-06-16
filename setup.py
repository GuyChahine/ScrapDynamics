from setuptools import setup
from scrapdynamics import __version__

install_requires = [
    "lxml>=4.9.2",
    "pandas>=2.0.2",
    "requests>=2.31.0",
    "rich>=13.4.2",
    "selenium>=4.10.0",
]

setup(
    name="scrapdynamics",
    version=__version__,
    url="https://github.com/guychahine/scrapdynamics",
    description="ScrapDynamics is a powerful framework for exploring and crawling websites.",
    long_description=open("./README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Guy Chahine",
    author_email="guychahine@gmail.com",
    packages=["scrapdynamics"],
    install_requires=install_requires,
    license="BSD",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
)
