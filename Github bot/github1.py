import os
import aiohttp
import csv
import datetime
from dateutil.tz import gettz

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

routes = web.RouteTableDef()
router = routing.Router()

@router.register("push")
async def issue_opened_event(event, gh, *args, **kwargs):
  #json_object = json.dumps(event.data, indent = 4)  
  print(event.data['repository']['full_name'])
  print(event.data['head_commit']['message'])
  print(event.data['head_commit']['timestamp'])
  print(event.data['head_commit']['author']['name'])
  print(event.data['head_commit']['author']['username'])
  print(event.data['head_commit']['added'])
  print(event.data['head_commit']['modified'])

  with open('update.csv', mode='a') as update_repo:
    update_writer = csv.writer(update_repo, delimiter=',')
    t = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
    update_writer.writerow([event.data['repository']['full_name'],event.data['head_commit']['message'],str(t.hour)+':'+str(t.minute)+':'+str(t.second),event.data['head_commit']['author']['name'],event.data['head_commit']['author']['username'],event.data['head_commit']['added'],event.data['head_commit']['modified']])

@routes.post("/")
async def main(request):
  body = await request.read()

  secret = "test-github-bot"
  oauth_token = "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"

  event = sansio.Event.from_http(request.headers, body, secret=secret)
  async with aiohttp.ClientSession() as session:
      gh = gh_aiohttp.GitHubAPI(session, "DishaVaidh",
                              oauth_token=oauth_token)
      await router.dispatch(event, gh)
  return web.Response(status=200)

def git():
  app = web.Application()
  app.add_routes(routes)
  port = os.environ.get("PORT")
  if port is not None:
    port = int(port)

  web.run_app(app, port=port)