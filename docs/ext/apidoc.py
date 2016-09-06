# https://github.com/openstack/deb-python-pycadf/blob/master/doc/ext/apidoc.py

import os.path as path

from sphinx import apidoc

run_already = False

def run_apidoc(app):
    global run_already
    if run_already:
        return
    run_already = True

    # Build CssefServer
    package_dir = path.abspath(path.join(app.srcdir, '..', '..', 'CssefServer'))
    source_dir = path.join(app.srcdir, 'autodoc', 'cssefserver')
    exclude_tests = path.abspath(path.join(app.srcdir, '..', '..', 'CssefServer', 'tests'))
    exclude_setup = path.abspath(path.join(app.srcdir, '..', '..', 'CssefServer', 'setup.py'))
    apidoc.main(['apidoc', package_dir, '-f', '-o', source_dir, exclude_tests, exclude_setup])

    # Build CssefClient
    package_dir = path.abspath(path.join(app.srcdir, '..', '..', 'CssefClient'))
    source_dir = path.join(app.srcdir, 'autodoc', 'cssefclient')
    exclude_tests = path.abspath(path.join(app.srcdir, '..', '..', 'CssefClient', 'tests'))
    exclude_setup = path.abspath(path.join(app.srcdir, '..', '..', 'CssefClient', 'setup.py'))
    apidoc.main(['apidoc', package_dir, '-f', '-o', source_dir, exclude_tests, exclude_setup])

def setup(app):
    app.connect('builder-inited', run_apidoc)