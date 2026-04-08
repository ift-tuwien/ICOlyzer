# Development

While not strictly required we assume that you installed:

- [`gh`](https://cli.github.com),
- [`just`](https://github.com/casey/just) and
- [`uv`](https://docs.astral.sh/uv)

in the description below.

## Test

Before you run the tests (on Linux and macOS) please make sure that you installed [`h5dump`](https://support.hdfgroup.org/documentation/hdf5/latest/_h5_t_o_o_l__d_p__u_g.html). After that use the following command:

```sh
just test
```

## Release

**Note:** Please replace `<VERSION>` with the version number e.g. `1.9.0` in the text below

To release a new version of ICOlyzer, please use the following steps:

1. Switch to the `main` branch

   ```sh
   git switch main
   ```

2. Check that the checks and tests finish successfully on Linux, macOS and Windows

   ```sh
   just
   ```

3. Check that the [**CI jobs** for the `main` branch finish successfully](https://github.com/ift-tuwien/ICOlyzer/actions)

4. Change the version number and commit your changes:

   ```sh
   just release <VERSION>
   ```

   **Note:** [GitHub Actions](https://github.com/ift-tuwien/ICOlyzer/actions) will publish a package based on the tagged commit and upload it to [PyPi](https://pypi.org/project/icotronic/).

5. Publish your release on GitHub:

   ```sh
   gh release create
   ```

   1. Choose the tag for the latest release
   2. As title use “Version `<VERSION>`”, e.g. “Version 1.9.0”
   3. Choose “Write my own”
   4. Paste the release notes for the latest version into the text editor window
   5. Save and close the text file
   6. Answer “N” to the question “Is this a prerelease?”
