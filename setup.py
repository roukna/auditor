from setuptools import setup

setup(name='auditor',
      version='1.0.0',
      description='Makes sure your CSV data is complian.',
      url='http://github.com/pfwhite/auditor',
      author='Patrick White',
      author_email='pfwhite9@gmail.com',
      license='Apache2.0',
      packages=['auditor'],
      entry_points={
          'console_scripts': [
              'auditor = auditor.__main__:main',
          ],
      },
      install_requires=['docopt', 'pyyaml', 'python-dateutil'],
      zip_safe=False)
