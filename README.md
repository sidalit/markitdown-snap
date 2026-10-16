# MarkItDown snap

[![markitdown](https://snapcraft.io/markitdown/badge.svg)](https://snapcraft.io/markitdown)

Snap packaging for [MarkItDown](https://github.com/microsoft/markitdown), a tool that converts PDF, Office documents, images, audio and other files to Markdown.

Unofficial build, not affiliated with or endorsed by Microsoft or the MarkItDown project.

## Build

```bash
snapcraft pack
```

## Install and try

<a href="https://snapcraft.io/markitdown"><img alt="Get it from the Snap Store" src="https://snapcraft.io/en/dark/install.svg" width="180"></a>

```bash
sudo snap install markitdown                   # or a local build: ./markitdown_0.1.8_*.snap --dangerous
sudo snap connect markitdown:removable-media   # optional: /media, /mnt
markitdown ~/Documents/report.pdf -o ~/Documents/report.md
printf '<h1>Hello</h1>' | markitdown -x html
```

## Test

After installing the snap, run the tests as a normal user:

```bash
python3 tests/smoke.py
```

They convert the sample files in `tests/fixtures` (copied from upstream) and check that FFmpeg and ExifTool start. They do not need network access.

## Known limitations

### Only amd64 and arm64

Magika, which MarkItDown uses to detect file types, needs ONNX Runtime, and ONNX Runtime publishes wheels for amd64 and arm64 only. The snap is built for these two.

### Hidden folders in your home directory

The snap cannot read or write hidden files or folders directly in your home directory, such as `~/.notes`. Use a normal folder, or pipe the file in:

```bash
cat ~/.notes/todo.html | markitdown -x html
```

### Audio transcription

Converting an audio file sends its audio to the Google Speech Recognition web service to transcribe it, so it needs network access. There is no option to turn this off.

### Azure services

Azure Document Intelligence (`-d`) needs an endpoint and credentials. Credentials from the Azure CLI on your system are not visible to the snap, so pass them as environment variables instead.

### Plugins

Third-party MarkItDown plugins cannot be installed into the snap. `--use-plugins` only finds the plugins bundled with it, which is none.

### ONNX Runtime warnings

Each run prints warnings from ONNX Runtime, such as `GPU device discovery failed` and `pthread_setaffinity_np failed`, because the sandbox hides hardware details and blocks pinning threads to CPUs. They are harmless and go to stderr only, so the Markdown output is not affected. Hide them with `2>/dev/null`.

## Update to a new upstream release

Change `version` and `source-tag` in `snap/snapcraft.yaml`, then rebuild.

## License

The packaging is MIT-licensed (see `LICENSE`). MarkItDown is MIT-licensed; its dependencies carry their own licenses.
