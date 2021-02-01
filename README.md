<a href="https://https://discord.gg/dtrpGnUPPb"><img src="https://img.shields.io/discord/738471115810406531?color=blue&label=Discord%20Server"/></a>

# iad

### iadpy is a wrapper for the [Im A Dev](https://im-a-dev.xyz) file uploader in python.

- Async wrapper (`async`, `await`)
- Proper rate limiting

## Usage

### Installation

Pypi
```
pip install iad
```

From GitHub
```
pip install git+https://github.com/Fxcilities/iad.py.git
```

### Examples

- Upload an image
```py
from iad import ImADev
from asyncio import get_event_loop

uploader = ImADev('token here')

async def main():
    with open('image.png', 'rb') as f:
        read = f.read()
        options = ('png', read)

        upload = await uploader.upload(options)
        print(upload.url)

loop = get_event_loop()
loop.run_until_complete(main())
```

- Getting a upload information
```py
from iad import ImADev
from asyncio import get_event_loop

uploader = ImADev('token here')

async def main():
    upload = await uploader.get_upload('filename.png')
    print(upload.url)

loop = get_event_loop()
loop.run_until_complete(main())
```