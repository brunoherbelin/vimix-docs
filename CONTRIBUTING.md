# Contributing to the vimix documentation

Thank you for helping! One page documents one feature. A contribution is one folder:

```
pages/<category>/<feature-name>/
    index.md
    img/<feature-name>-01.png
    img/<feature-name>-02.png
```

- `<category>`: an existing folder in `pages/` (e.g. `getting-started`, `sources`, `mixing`, `output`), or propose a new one in your pull request.
- `<feature-name>`: lowercase words separated by dashes, e.g. `loopback-source`.

## 1. Write the page

Copy `_template/index.md` and fill in:

| Front matter | Content |
|---|---|
| `title` | Name of the feature |
| `summary` | One sentence on what it does |
| `author` | Your name or GitHub handle |
| `vimix_version` | The version you tested with (menu *About*) |
| `date` | Date of writing, `YYYY-MM-DD` |

Then the three sections:

- **What it does**: 2 to 4 sentences, no jargon.
- **How to**: numbered steps, one user action per step, each with a screenshot when useful.
- **Specific information**: shortcuts, limitations, platform differences, links to related pages.

## 2. Make the screenshots

1. Take a screenshot of the vimix window (or of the relevant part).
2. Use the vimix **Annotation** feature to add arrows, circles and text on the interface elements to act on.
3. Export the result as PNG.

Rules (checked automatically on pull requests):

- PNG only. Do not worry about size: after merge, screenshots wider than 1600 px or heavier than 300 KB are resized and compressed automatically (you can run `python3 scripts/optimize_images.py` yourself, it needs Pillow).
- File name: `<feature-name>-NN.png`, numbered in order of appearance.
- Always write an alt text: `![Click the + button to add a source](img/feature-01.png)`.
- Keep the default vimix theme so images stay consistent.

## 3. Submit

**From the web interface (no git needed)**

1. Click *Fork* on this repository.
2. In your fork: *Add file* > *Upload files*, drag your folder content (keep the folder structure), then commit.
3. Click *Contribute* > *Open pull request* and fill the checklist.

**With git**

```
git clone https://github.com/<you>/vimix-docs && cd vimix-docs
git switch -c doc/<feature-name>
cp -r _template pages/<category>/<feature-name>
# edit, add images
git add pages && git commit -m "Add <feature-name> page" && git push -u origin HEAD
```

**Without a pull request**: open an issue with the *Documentation proposal* form and attach your markdown and a zip of the images. A maintainer will add it for you, crediting you as author.

## 4. Review

A maintainer checks accuracy, template and image rules, and may ask for changes. Once merged, the website is rebuilt automatically.

You can run the same checks locally: `python3 scripts/check_pages.py`.
