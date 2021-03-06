This is a learning project for learning full stack test driven development and the Django web framework.  It is based on the book "Test-Driven Development with Python" by Harry J.W. Percival.

Tests can be run with:

  $ python manage.py test

Functional tests can be run against a live, deployed environment with:

  $ STAGING_SERVER="your.web.address"  python manage.py test functional_tests --failfast

Deployments are performed with:

  $ fab -f deploy_tools/fabfile.py deploy:host=username@your.web.address

The necessary requirements for running the server are in requirements.txt.  Other libraries that are necessary for testing or useful for local development are in dev-requirements.txt.

To run the functional_tests, you'll need to install geckodriver.
