from distutils.core import setup
import py2exe
import glob
import os

includes = ['scrapy','scrapy.*','selenium','selenium.*','lxml','lxml.*','OpenSSL','OpenSSL.*','ENGIN_144.*','twisted.*']

options = {"py2exe":
               {"compressed": 1,
                "optimize": 2,
                # "includes": includes,
                # "bundle_files": 1,
                "ascii": 1,
                }}

setup(
    data_files=[(".", ["scrapy.cfg"]),
                ("ENGIN_144", glob.glob("ENGIN_144\\*.*")),
                ("ENGIN_144\\spiders", glob.glob("ENGIN_144\\spiders\\*.*")),
                ("ENGIN_144\\MyMiddle", glob.glob("ENGIN_144\\MyMiddle\\*.*")),
                ],
    options=options,
    console=["GooglePlay-Spider.py"],
    # zipfile=None,
)