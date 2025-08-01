from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='primestg',
    version='1.56.6',
    packages=find_packages(),
    url='https://github.com/gisce/primestg',
    license='GNU Affero General Public License v3',
    author='GISCE-TI, S.L.',
    author_email='devel@gisce.net',
    install_requires=[
        'lxml',
        'zeep<4.0',
        'libcomxml',
        'python-dateutil'
    ],
    description='Prime STG-DC Interface Specification',
    long_description=readme,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
      ],
    entry_points = '''
       [console_scripts]
       primestg=primestg.cli:primestg
    ''',
)
