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
    pip install -r requirements

Generating a sitemap
-----------------------------

::

    $ ./bin/spider

Because this can take a while I've included a sample `sitemap.yaml`
that can be used to immediately generate traffic.


Using that sitemap to generate requests against a site
------------------------------------------------------------

::

    ./bin/traffic http://godzilla.threadless.com

