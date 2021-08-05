import pytz

from datetime import date, datetime, timedelta, tzinfo

import constants

class Game(object):
  def __init__(self, data):
    self.data = data
    self.timezone = pytz.timezone('Zulu')

  def __str__(self):
    return self.short_summary

  @property
  def home_team_abbr(self):
    return constants.TEAMS[self.data['teams']['home']['team']['id']]['abbr']

  @property
  def away_team_abbr(self):
    return constants.TEAMS[self.data['teams']['away']['team']['id']]['abbr']

  @property
  def home_score(self):
    return self.data['teams']['home']['score']

  @property
  def away_score(self):
    return self.data['teams']['away']['score']

  @property
  def game_state(self):
    return int(self.data['status']['statusCode'])

  @property
  def in_progress(self):
    if self.game_state in [constants.GAME_STATE_PREGAME, constants.GAME_STATE_IN_PROGRESS, constants.GAME_STATE_CRITICAL]:
      return True
    else:
      return False

  @property
  def current_period(self):
    return self.data['linescore']['currentPeriod']

  @property
  def current_period_ordinal(self):
    return self.data['linescore']['currentPeriodOrdinal']

  @property
  def game_over(self):
    if self.game_state in [constants.GAME_STATE_OVER, constants.GAME_STATE_FINAL, constants.GAME_STATE_FINAL2]:
      return True
    else:
      return False

  @property
  def final_abbr(self):
    if self.current_period <= 3:
      # Ended in regulation
      return 'F'
    elif self.current_period == 4:
      # Overtime
      return 'F/OT'
    elif self.current_period == 5:
      # Shootout
      return 'F/SO'
    else:
      # Dunno?
      return 'F'

  @property
  def short_summary(self):
    if self.game_over:
      return '{} {} @ {} {} {}'.format(self.away_team_abbr, self.away_score, self.home_team_abbr, self.home_score, self.final_abbr)
    elif self.in_progress:
      if self.current_period > 3:
        return '{} {} @ {} {} {}'.format(self.away_team_abbr, self.away_score, self.home_team_abbr, self.home_score, self.current_period_ordinal)
      else:
        return '{} {} @ {} {}'.format(self.away_team_abbr, self.away_score, self.home_team_abbr, self.home_score)
    else:
      # Hasn't Started
      return '{} @ {} {}'.format(self.away_team_abbr, self.home_team_abbr, self.start_time_eastern)

  @property
  def date_as_iso(self):
    d = datetime.strptime(self.data['gameDate'], "%Y-%m-%dT%H:%M:%SZ")
    return d.date().isoformat()

  @property
  def start_time_eastern(self):
    d = datetime.strptime(self.data['gameDate'], "%Y-%m-%dT%H:%M:%SZ")
    d_aware = self.timezone.localize(d)
    eastern_time = d_aware.astimezone(pytz.timezone('US/Eastern'))
    if eastern_time.hour > 12:
      if eastern_time.minute > 0:
        return "{}:{}PM ET".format(eastern_time.hour - 12, eastern_time.minute)
      else:
        return "{}PM ET".format(eastern_time.hour - 12)
    else:
      if eastern_time.minute > 0:
        return "{}:{}AM ET".format(eastern_time.hour, eastern_time.minute)
      else:
        return "{}AM ET".format(eastern_time.hour)
