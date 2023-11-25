from distutils.core import setup


setup(
    name='SPPy',
    verson='0.1.0',
    author='Moin Ahmed',
    author_email='moinahmed100@gmail.com',
    packages=['SPPy', 'test'],
    install_requires=['numpy', 'pandas', 'scipy', 'tqdm', 'matplotlib', 'pytest', 'django', 'bokeh']
)