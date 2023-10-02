![](./.github/banner.png)

<p align="center">
    A small C/C++ library to lookup Windows error codes.
    <br>
    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/p0dalirius/win32errorcodes">
    <a href="https://twitter.com/intent/follow?screen_name=podalirius_" title="Follow"><img src="https://img.shields.io/twitter/follow/podalirius_?label=Podalirius&style=social"></a>
    <a href="https://www.youtube.com/c/Podalirius_?sub_confirmation=1" title="Subscribe"><img alt="YouTube Channel Subscribers" src="https://img.shields.io/youtube/channel/subscribers/UCF_x5O7CSfr82AfNVTKOv_A?style=social"></a>
    <br>
</p>

## Usage:

### In C / C++

```c
const char* lookup_errorA(unsigned long errcode);
const wchar_t* lookup_errorW(unsigned long errcode);
```

## In Python

```python
def win32_lookup_error(errcode:int) -> str;
```

## Contributing

Pull requests are welcome. Feel free to open an issue if you want to add other features.
