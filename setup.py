import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

    setuptools.setup(

     name='realpy',  

     version='0.2',

     scripts=['realpy.sh'] ,

     author="Martin van Leeuwen",

     author_email="martinvanleeuwen95@gmail.com",

     description="Real time video and graphs with python backend and fable frontend",

     long_description=long_description,

     long_description_content_type="text/markdown",

     url="https://github.com/martinchristiaan/realpy",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

 )
