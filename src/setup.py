from distutils.core import setup

setup(
    name='wintoastlistener',
    version='1.0.0',
    author='Gu-f',
    packages=['src/toast_listener'],
    scripts=[],
    url='https://github.com/Gu-f/WinToastListener',
    license='LICENSE',
    description='A python library implemented by python3, for listening to Toast message notifications on windows.',
    long_description=open('README_EN.md', encoding="utf-8").read(),
    install_requires=[
        "pywin32~=308",
    ],
)