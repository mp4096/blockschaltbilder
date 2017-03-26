from setuptools import setup


setup(
    name="Blockschaltbilder",
    version="0.1",
    description="Blockschaltbilder: Boilerplate code generator",
    author="Mikhail Pak",
    author_email="mikhail.pak@tum.de",
    url="https://github.com/mp4096/blockschaltbilder",
    packages=["blockschaltbilder"],
    install_requires=["numpy"],
    license="MIT",
    test_suite="blockschaltbilder.tests",
    )
