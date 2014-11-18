from setuptools import find_packages, setup


install_requires = ['wsgiref']


setup(name='httpserver',
      version='0.0.1',
      description='Simple HTTP server',
      platforms=['POSIX'],
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      entry_points={
          'console_scripts': [
              'httpserver = httpserver.main:main',
              'httpserver_tests = httpserver.tests:main',
              ]},
      zip_safe=False)
