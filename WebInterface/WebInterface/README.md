# Development Documentation

This is built so that a framework of site resources is provided at the root of the project. These resources are as follows:
* Contexts
* Utils
* Templates

A site component should have all of its necessary resources stored within a directory of its own, which is then placed under the modules directory. Then link to that modules from the root urls.py. For example, the 'administrator' module is referenced by the following line:

```python
url(r'^admin/',			include('WebInterface.modules.administrator.urls')),
```

The administrator module provides it's own urls file. It also has its own:
* context.py
* forms.py
* view.py
* templates folder

Each file utilizes the base resources provided in the root of the project. For instance, the 'adminPageTemplate.html' which is used as a template for the rest of the admin pages, actually extends the 'sitePageTemplate.html' file within the root templates folder.

See the README.md in each module for more information about that particular module.