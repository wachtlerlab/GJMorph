from setuptools import setup, find_packages
setup(
    name="GJMorph",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(exclude=["^\."]),
    exclude_package_data={'': ["Readme.md"]},
    install_requires=["numpy>=1.11.2",
                      "matplotlib>=1.5.3",
                      "scipy>=0.18.1",
                      "pandas>=0.19.0",
                      "seaborn>=0.7.1",
                      "pylatex",
                      "btmorph2>=2.1.1",
                      "pillow>=4.0.0",
                      "xlrd>=1.0.0",
                      "openpyxl>=2.4.5",
                      "scikit-learn>=0.18.1",
                      "regmaxsn",
                      "requests>=2.14.2",
                      "py-vaa3d>=0.1",
                      "scikit-learn>=0.19.1"],

    python_requires=">=2.7",
    dependency_links=["git+https://github.com/wachtlerlab/btmorph_v2.git",
                      "git+https://github.com/dEvasEnApati/pyVaa3d.git"]


    )