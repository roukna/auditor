from setuptools import setup

with open('auditor/version.py') as ver:
    exec(ver.read())

setup(name='auditor',
      version=__version__,
      description='Makes sure your CSV data is complian.',
      url='http://github.com/pfwhite/auditor',
      author='Patrick White',
      author_email='pfwhite9@gmail.com',
      license='Apache2.0',
      packages=['auditor'],
      entry_points={
          'console_scripts': [
              'auditor = auditor.__main__:cli_run',
          ],
      },
      install_requires=[
          'docopt==0.6.2',
          'pyyaml==3.12',
          'python-dateutil==2.6.1'],
      zip_safe=False)
