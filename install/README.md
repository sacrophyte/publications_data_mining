# Installation notes
How to set up your environment to run these scripts

## Python environment
Those who are running from a Unix-based environment will probably have an easier time with this. However, the instructions here assume a Windows environment.

I started with Anaconda (https://www.anaconda.com/download/), since it was recommended for the Scopus API I was using at the time.
I created a new Environment (I called mine "scopus"). From this new environment, I "Open Terminal", which gives me a shell for running pyton. In this environment, I have accumulated a number of modules, but here are all the modules I import for Experts:
- from boxsdk import Client, OAuth2
- re, html2text, requests, json, numpy

I also created a projects directory under c:\Users\%user%, and in that project directory I store the python scripts and all generated output. I also store the app.cfg here that is needed for the box.com api keys.

I use the IDLE editor that comes with Anaconda to work with python files.

When I am ready to run a python script, I execute it in the python shell (see above for the environment):  
**python my_python_script.py**
