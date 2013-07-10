Spinneret
-----------------------------

Spinneret is a web spider and dynamic load generator for testing,
benchmarking, and warming caches.

Setup
-----------------------------

::

    git clone git@github.com:steder/spinneret.git
    cd spinneret
    mkdir -p ~/.virtualenvs
    virtualenv ~/.virtualenvs/spinneret
    python setup.py develop



Generating a sitemap
-----------------------------

::

   spinneret spider --base_url http://localhost:8000

Because this can take a while I've included a sample `sitemap.yaml`
that can be used to immediately generate traffic.


Using that sitemap to generate requests against a site
------------------------------------------------------------

::

   spinneret traffic --base_url http://localhost:8000 --inflight 100
