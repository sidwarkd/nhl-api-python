import os
import requests

import models

API_ROOT = 'https://statsapi.web.nhl.com/api/v1/'

class Api(object):
  def __init__(self):
    pass

  def call(self, resource, query):
    response = requests.get('{}{}?{}'.format(API_ROOT, resource, query))
    return response.json()

  def get_games_for_date(self, date):
    result = self.call('schedule', 'startDate={}&endDate={}&expand=schedule.linescore'.format(date.date().isoformat(), date.date().isoformat()))
    dates = result["dates"]
    if len(dates) == 0:
      return None
    else:
      # Return the games sorted by game state so those finished or in progress
      # come first. The API returns them sorted but in case this changes we
      # sort them here
      return sorted((models.Game(game_data) for game_data in dates[0]['games']), key=lambda x: x.game_state, reverse=True)

  def get_games_for_date_range(self, startDate, endDate):
    result = self.call('schedule', 'startDate={}&endDate={}&expand=schedule.linescore'.format(startDate.date().isoformat(), endDate.date().isoformat()))
    dates = result["dates"]
    if len(dates) == 0:
      return None
    else:
      # Return the games sorted by game state so those finished or in progress
      # come first. The API returns them sorted but in case this changes we
      # sort them here
      return sorted((models.Game(game_data) for game_data in dates[0]['games']), key=lambda x: x.game_state, reverse=True)