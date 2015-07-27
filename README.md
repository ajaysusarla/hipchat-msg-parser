# HipChat Message Parser #
HipChat message parser, looks at a given message for `@mentions`, `emoticons` and `links` and presents the parsed content in JSON.


## Dependencies ##
`parse-msg` has been tested to work with `python2.7` and depends on the following packages:

* [rfc3987](https://pypi.python.org/pypi/rfc3987/) - For validating URI's.
* [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4)  - For parsing HTML.
* [futures.concurrent](https://docs.python.org/3/library/concurrent.futures.html) - For fetching titles of http/https links parallely.

These packages are listed in `requirements.txt`. To install the dependencies, please run:

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
The `tests/example-data.txt` file has several examples, that can be used to test `parse-msg`. One can edit the file and add test data to it. Example usage:
```bash
$ ./parse-msg < tests/example_data.txt
Input:  @chris you around?
Ouput:
{
  "mentions": [
    "chris"
  ]
}

Input:  Olympics are starting soon; http://www.nbcolympics.com
Ouput:
{
  "links": [
    {
      "url": "http://www.nbcolympics.com",
      "title": "NBC Olympics | Home of the 2016 Olympic Games in Rio"
    }
  ]
}

Input:  @bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016
Ouput:
{
  "mentions": [
    "bob",
    "john"
  ],
  "emoticons": [
    "success"
  ],
  "links": [
    {
      "url": "https://twitter.com/jdorfman/status/430511497475670016",
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
And then can be installed in the appropriate python site-packages directory.

## Unit Tests ##
Unit tests can be found in the tests/ directory. To run the unit tests, just run `tox` from the top-level project directory.
