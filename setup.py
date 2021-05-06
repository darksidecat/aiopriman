from setuptools import setup

setup(
    name='aiopriman',
    packages=['aiopriman'],
    version='0.1.1',
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
