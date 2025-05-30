# Mkdocs Framework and Material Theme for the kluster.ai Docs

This repo contains the Mkdocs config files, theme overrides, and custom CSS for the [kluster.ai](https://kluster.ai) documentation site.

- [Mkdocs](https://www.mkdocs.org/)
- [Material for Mkdocs](https://squidfunk.github.io/mkdocs-material/)

The actual content is stored in the docs repo and pulled into the docs directory during build.

- [Docs](https://github.com/kluster-ai/docs)

## Install Dependencies

To get started, you need to install [mkdocs](https://www.mkdocs.org/). All dependencies, including mkdocs, can be installed with a single command; you can run:

```bash
pip install -r requirements.txt
```

## Getting Started

For everything to work correctly, the file structure needs to be as follows:

```text
kluster-mkdocs
|--- /material-overrides/ (folder)
|--- /kluster-docs/ (folder)
|--- mkdocs.yml
```

To set up the structure, follow these steps:

1. Clone this repository:

    ```bash
    git clone https://github.com/papermoonio/kluster-mkdocs
    ```

2. Inside the folder just created, clone the [docs repository](https://github.com/kluster-ai/docs), **note that we force the output to be kluster-docs**:

    ```bash
    cd kluster-mkdocs
    git clone https://github.com/kluster-ai/docs kluster-docs
    ```

3. In the `kluster-mkdocs` folder (which should be the current one), you can build the site by running:

    ```bash
    mkdocs serve
    ```

After a successful build, the site should be available at `http://127.0.0.1:8000`.

## Editing Theme Files

If you're editing any of the files in the `material-overrides` directory, you can run the following command to watch for these changes and render them automatically:

```bash
mkdocs serve --watch-theme
```

Otherwise, you'll need to stop the server (`control + C`) and restart it (`mkdocs serve`) to see the changes.

## Issues Converting Notebooks

If you run into the following issue when converting a notebook:

```
metadata["widgets"][WIDGET_STATE_MIMETYPE]["state"]
KeyError: 'state'
```

This is due to some problems when rendering widgets. To circunvent the issue, you can run the following:

```
jq -M 'del(.metadata.widgets)' your-file.ipynb > your-file-fixed.ipynb
```

Check the `fixed` file, confirm the changes and then rename accordingly.

## Updating Documentation

The project includes a unified tool for updating documentation components when API changes or new models are released:

```bash
# Update all documentation components
python scripts/kluster_model_update/update_docs.py

# Test commands 
python scripts/kluster_model_update/update_docs.py --dry-run
```

For more details, see [kluster-docs Documentation Update Tool](/scripts/kluster_model_update/README.md.)