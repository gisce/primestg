from setuptools import setup, find_packages


setup(
    name='primestg',
    version='0.2.0',
    packages=find_packages(),
    url='https://github.com/gisce/primestg',
    license='GNU Affero General Public License v3',
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    install_requires=[
        'lxml'
    ],
    description='Prime STG-DC Interface Specification'
)
