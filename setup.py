import setuptools

setuptools.setup(
    name='scrapybox',
    version='0.1',
    license='BSD',
    url='https://github.com/stav/scrapybox',
    download_url='https://github.com/stav/scrapybox/archive/master.zip',
    description='A Scrapy GUI',
    long_description=open('README').read(),
    author='Steven Almeroth',
    author_email='sroth77@gmail.com',
    maintainer='Steven Almeroth',
    maintainer_email='sroth77@gmail.com',
    install_requires=['aiohttp', 'aiohttp-jinja2', 'cchardet'],
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    package_data={"": ["LICENSE", "README"]},
    include_package_data=True,
    keywords=[
        'scrapy',
        'async',
        'server',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Scrapy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': ['sbserve = scrapybox.server.server:main']
    },
)
