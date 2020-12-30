# XNXX Scrape

Scrape [xnxx](https://xnxx.com) dengan pyppeteer dan BeautifulSoup 4 Python

# Routes

`/videos` = Beberapa Video dari halaman beranda.
`/videos/<video_name>` = Mencari video.

# Output

## videos
```
[{
  "title": String,
  "url": String,
  "thumbnail": String
}, {
  ...
}]
```

## videos/<video_name>

### Success
```
{
  "success": true,
  "message": "Success 200",
  "result": [
    {
      "title": String,
      "url": String,
      "thumbnail": String,
      "metadata": {
        "duration": String
      }
    }, {
      ...
    }
  ]
}
```
### Fail
```
{
  "success": false,
  "message": "Not found"
}
```