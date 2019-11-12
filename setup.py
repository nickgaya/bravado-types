import os.path

from setuptools import setup

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='bravado-types',
    use_scm_version=True,
    license="MIT License",
    description="Tool to generate MyPy type stubs for Bravado-generated "
                "classes to support static type checking.",
    author="Nicholas Gaya",
    author_email="nickgaya@users.noreply.github.com",
    url="https://github.com/nickgaya/bravado-types",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["bravado_types"],
    package_data={
        'bravado_types': ['py.typed', 'templates/*.mako'],
    },
    # According to the documentation, this is needed to ensure MyPy can
    # detect the py.typed file. See
    # https://mypy.readthedocs.io/en/latest/installed_packages.html
    zip_safe=False,
    classifiers=[
        "Topic :: Software Development :: Code Generators",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Typing :: Typed",
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=[
        'bravado>=10.3.0',
        'bravado-core>=5.14.0',
        # Template rendering library
        'mako',
        # Used for accessing package resources
        'setuptools',
    ],
    entry_points={
        'console_scripts': [
            'bravado-types = bravado_types.__main__:main',
        ],
    },
)
