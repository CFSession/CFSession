from setuptools import setup
with open('README.md', 'rt') as readme:
    long_description = readme.read()

setup(
    name='CFSession',
    version='1.3.0a0',
    author='Kinuseka',
    author_email='realkingseeker1089@gmail.com',
    description='A Cloudflare IUAM session grabber',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Kinuseka/CFSession',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'Typing :: Typed'
    ],
    install_requires=[
        'requests>=2.25.0',
        'undetected-chromedriver>=3.1.6,!=3.5.1'
    ],
    packages=['CFSession'],
    python_requires=">=3.6",
    license="Apache-2.0"
)
