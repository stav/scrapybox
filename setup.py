import setuptools

setuptools.setup(
    name='Scrapybox',
    version='0.1',
    url='https://github.com/stav/scrapybox',
    description='A RESTful async Python web server that runs arbitrary spider code.',
    long_description=open('README').read(),
    author='Steven Almeroth',
    maintainer='Steven Almeroth',
    maintainer_email='sroth77@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    include_package_data=False,
    entry_points={
        'console_scripts': ['sbserve = scrapybox.server.server:main']
    },
)
