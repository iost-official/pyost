from distutils.core import setup
setup(
  name = 'pyost',         # How you named your package folder (MyLib)
  packages = ['pyost','pyost.rpc.pb'],   # Chose the same as "name"
  version = 'v3.0',      # Start with a small number and increase it with every change you make
  license='LGPG',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python SDK for the IOST Blockchain',   # Give a short description about your library
  long_description= 'Python SDK for the IOST Blockchain',
  author = 'Cyril Clement',                   # Type in your name
  author_email = 'dossiman@domain.com',      # Type in your E-Mail
  url = 'https://github.com/dossiman/pyost',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/dossiman/pyost/archive/v2.2-beta.tar.gz',    # I explain this later on
  keywords = ['IOST', 'blockchain', 'API', 'SDK'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
    'base58',
    'ecdsa',
    'ed25519',
    'grpcio',
    'googleapis-common-protos',
    'protobuf3-to-dict'],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Programming Language :: Python :: 3.7',
  ],
)
