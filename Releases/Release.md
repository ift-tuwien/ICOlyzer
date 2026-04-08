# Release

To release a new version of ICOlyzer, please use the following steps:

1. Check that the [**CI jobs** for the `main` branch finish successfully](https://github.com/ift-tuwien/ICOlyzer/actions)
2. Create a new release [here](https://github.com/ift-tuwien/ICOlyzer/releases/new)
   1. Open the [release notes](.) for the latest version (e.g. [`1.5.0.md`](1.5.0.md))
   2. Replace links with a permanent version:

      For example instead of
      - `../../something.txt` use
      - `https://github.com/ift-tuwien/ICOlyzer/blob/REVISION/something.txt`,

      where `REVISION` is the latest commit hash of the `main` branch (e.g. `e10daa7d` for version `1.4.0`)

   3. Commit your changes
   4. Copy the release notes
   5. Paste them into the main text of the release web page
   6. Decrease the header level of each section by two
   7. Remove the very first header
   8. Check that all links work correctly

3. Change the value of `version` in [`pyproject.toml`](../pyproject.toml) and commit your changes
4. Push the latest commits
5. Build and upload the package to PyPI:
   1. Install [`build`](https://pypi.org/project/build/):

      ```sh
      python3 -m pip install --upgrade build
      ```

   2. Build package:

      ```sh
      python3 -m build
      ```

   3. Install [`twine`](https://pypi.org/project/twine/)

      ```sh
      python3 -m pip install --upgrade twine
      ```

   4. Upload package to PyPI:

      ```sh
      python3 -m twine upload dist/*
      ```

6. Insert the version number (e.g. `1.5.0`) into the tag field
7. For the release title use “Version VERSION”, where `VERSION` specifies the version number (e.g. “Version 1.5.0”)
8. Click on “Publish Release”
