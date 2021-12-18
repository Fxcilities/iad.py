<a href="https://https://discord.gg/dtrpGnUPPb"><img src="https://img.shields.io/discord/738471115810406531?color=blue&label=Discord%20Server"/></a>

# iad

### iadpy is a wrapper for the [monke.cc](https://monke.cc) file uploader in python.

- Async wrapper (`async`, `await`)
- Proper rate limiting

## Usage

### Installation

Pypi
```
pip install iad.py
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
from io import BytesIO

uploader = ImADev('token here')

async def main():
    # from file path
    upload = await uploader.upload('image.png')
    print(upload.url)
    
    # from bytes
    upload = await uploader.upload(bytes_here, file_format='png')
    print(upload.url)
    
    # from buffer
    upload = await uploader.upload(BytesIO(), file_format='png')
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
