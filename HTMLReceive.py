import asyncio
from pyppeteer import launch

async def receive(url: str):
  browser = await launch(
    handleSIGINT=False,
    handleSIGTERM=False,
    handleSIGHUP=False,
    args=['--no-sandbox']
  )
  page = await browser.newPage()
  await page.goto(f"{url}")
  
  html = await page.evaluate('''() => {
    return document.body.innerHTML;
  }''')
  
  await page.close()
  await browser.close()
  return html


def r(url: str, loop):
  asyncio.set_event_loop(loop)
  task = loop.create_task(receive(url))
  value = loop.run_until_complete(task)
  loop.close()
  return value