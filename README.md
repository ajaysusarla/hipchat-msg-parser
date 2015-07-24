# HipChat Message Parser #
HipChat message parser, looks at a given message for `@mentions`, `emoticons` and `links` and presents the parsed content in JSON.


## Dependencies ##
`parse-msg` depends on the following packages:
* [rfc3987](https://pypi.python.org/pypi/rfc3987/) - For validating URI's.
* [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4)  - For parsing HTML.

These packages are listed in `requirements.txt`.
To install the dependencies, please run:

```bash
pip install -r requirements.txt
```

## Usage ##
```bash
$ echo "Calling @foo for (coffee) at http://some-place.com/location" | ./parse-msg
Input:  Calling @foo for (coffee) at http://some-place.com/location
Ouput:
{
  "mentions": [
    "foo"
  ],
  "emoticons": [
    "coffee"
  ],
  "links": [
    {
      "url": "http://some-place.com/location", 
      "title": ""
    }
  ]
}

```


## Installing ##
A gzipped tarball of this project can be build by running:
```bash
./setup.py bdist
```
And then can be installed in an appropriate python site-packages directory.