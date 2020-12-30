import asyncio
from HTMLReceive import r
from bs4 import BeautifulSoup
from flask import Flask, current_app, jsonify
import json

app = Flask(__name__)

def homeVideos():
  loop = asyncio.new_event_loop()
  html = r('https://xnxx.com', loop)
  soup = BeautifulSoup(html, "html5lib")
  videos_element = soup.find('div', class_="mozaique").parent.find_all('div', class_="thumb-block thumb-cat")
  videos = []
  for video in videos_element:
    if video.find('p', class_="title").text.strip() != "Today's selection":
      title = video.find('p', class_="title").text.strip()
      url = video.find('p', class_="title").findNext('a').attrs['href']
      thumbnail = video.find('img').attrs['src']
      url = f"https://xnxx.com{url}"

      videos.append({
        "title": title,
        "url": url,
        "thumbnail": thumbnail
      })
  return videos

def searchVideos(videoName: str):
  loop = asyncio.new_event_loop()
  html = r(f"https://www.xnxx.com/search/{videoName}", loop)

  soup = BeautifulSoup(html, "html5lib")
  videos = []
  if soup.find(class_="mozaique") == None:
    return None
  else:
    videos_element = soup.find(class_="mozaique").find_all(class_="thumb-block")
    for video in videos_element:
      url = video.find('div', class_="thumb").findNext('a').attrs['href']
      url = f"https://xnxx.com{url}"
      thumbnail = video.find('div', class_="thumb").findNext('img').attrs['src']
      title = video.find('div', class_="thumb-under").findNext('p').text.strip()
      metadata = {
        "duration": video.find('div', class_="thumb-under").find('p', class_="metadata").contents[1].strip()
      }
      videos.append({
        "title": title,
        "url": url,
        "thumbnail": thumbnail,
        "metadata": metadata
      })
  return videos

@app.route("/")
def home():
  return jsonify({
    "hello": "world"
  })

@app.route("/videos")
def hVideos():
  return current_app.response_class(json.dumps(homeVideos(), indent=4), mimetype="application/json")

@app.route("/videos/<video_name>")
def sVideos(video_name):
  result = searchVideos(str(video_name))
  if result == None:
    return jsonify({ "success": False, "message": "Not found" })
  else:
    return current_app.response_class(json.dumps({ "success": True, "message": "Success 200", "result": result }, indent=4), mimetype="application/json")

if __name__ == "__main__":
  app.run(
    host="0.0.0.0",
    port=9271
  )