# Documentation setup

## Build Dependencies
Sphinx documentation generation is done via Make. You will need sphinx and sphinx_rtd_theme installed:
```bash
pip install sphinx sphinx_rtd_theme
```

## Build Process
You can use the make file as you would with any other sphinx project.
```
make html
```

If you are actively working on documentation, you can watch the project directories for changes and regenerate the documentation when modifications are seen.

```
while inotifywait -e modify -r ../CssefServer/; do make html; done
```

Take advantage of pythons SimpleHTTPServer to make reviewing the changes easier:
```
cd docs/build/html
python -m SimpleHTTPServer
```