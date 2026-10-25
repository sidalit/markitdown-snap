<div align="center">

# MarkItDown

**Convert documents, images and audio to Markdown.**

[![markitdown](https://snapcraft.io/markitdown/badge.svg)](https://snapcraft.io/markitdown)
[![Base: core26](https://img.shields.io/badge/Base-core26-2C8C3C?logo=canonical&logoColor=white)](https://snapcraft.io/core26)
![Confinement: strict](https://img.shields.io/badge/Confinement-strict-2C8C3C)
[![Maintainer: sidaliteir](https://img.shields.io/badge/Maintainer-sidaliteir-2C8C3C?logo=snapcraft&logoColor=white)](https://snapcraft.io/publisher/sidaliteir)
![Architectures: amd64 and arm64](https://img.shields.io/badge/Architectures-amd64%20%7C%20arm64-2C8C3C?logo=linux&logoColor=white)

[Getting Started](#getting-started) · [Configure](#configure) · [Limitations](#limitations) · [Build](#build) · [Support](#support) · [License](#license)

Unofficial snap packaging for [MarkItDown](https://github.com/microsoft/markitdown), a converter for PDF, Office documents, HTML, images, audio and other files.

</div>

---

## Getting Started

<a href="https://snapcraft.io/markitdown"><img alt="Get it from the Snap Store" src="https://snapcraft.io/en/dark/install.svg" width="180"></a>

```bash
sudo snap install markitdown
markitdown ~/Documents/report.pdf -o ~/Documents/report.md
```

You can also pipe content into the converter:

```bash
printf '<h1>Hello</h1>' | markitdown -x html
```

## Configure

This snap has no `snap set` options. Choose conversion options with `markitdown --help`.

```bash
sudo snap connect markitdown:removable-media   # optional: /media, /mnt
```

Azure Document Intelligence (`-d`) requires an endpoint and credentials. Supply Azure credentials through environment variables; the snap cannot use your host Azure CLI login.

## Limitations

- Hidden files directly under your home directory are inaccessible. Use a normal folder, or pipe the file into `markitdown`.
- Audio transcription sends audio to Google's Speech Recognition service and requires network access; there is no offline switch.
- Third-party plugins cannot be installed into the snap. No optional MarkItDown plugins are bundled.
- ONNX Runtime may warn about GPU discovery or CPU affinity under confinement. These warnings go to stderr and do not alter the Markdown output.

## Build

```bash
git clone https://github.com/sidalit/markitdown-snap.git
cd markitdown-snap
sudo snap install snapcraft --classic
snapcraft pack
```

## Support

- **Installation or snap issues:** [open a packaging issue](https://github.com/sidalit/markitdown-snap/issues).
- **Application bugs:** [report them upstream](https://github.com/microsoft/markitdown/issues).

## License

Snap packaging: [MIT](https://github.com/sidalit/markitdown-snap/blob/main/LICENSE).
