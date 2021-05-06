import sys

from setuptools import setup, find_packages

# Check python version
MINIMAL_PY_VERSION = (3, 7)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('aiopriman works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))

setup(
    name='aiopriman',
    packages=find_packages(exclude=('tests', 'tests.*', 'examples.*', 'docs',)),
    version='0.1.3',
    license='MIT',
    description='library for managing asyncio synchronization primitives',
    author='darksidecat',
    author_email='bitalik371@gmail.com',
    url='https://github.com/darksidecat/aiopriman',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    include_package_data=False,
)
