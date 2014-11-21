#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import common
import randcpu

def play():
  # 全てがランダムな場合、大体71.5% vs 28.5%で姫騎士が有利
  actions = common.rand_ordered_action_list()
  g = common.Game(common.rand_field_seq())
  for action in actions:
    func = randcpu.strategy(g, action)
    g.update(action, func)
  return (g, actions) 

def test():
  print   logging.basicConfig(level=logging.DEBUG)
  g = common.Game([1,2,2,2,1,0], [2,3], ['strong_violence', 'change', 'draw'])
  print g
  for key in ['revenge']:
    func = randcpu.strategy(g, key)
    g.update(key, func)
  print g

if __name__ == '__main__':
  win = 0
  lose = 0
  win_actions = {}
  lose_actions = {}
  for i in xrange(0, 100000):
    (g, action_list) = play()
    actions = str(action_list)
    if g.is_princess_win():
      win = win + 1
      # win_actions[actions] = win_actions[actions] + 1 if win_actions.has_key(actions) else 1
    else:
      lose = lose + 1
      # lose_actions[actions] = lose_actions[actions] + 1 if lose_actions.has_key(actions) else 1
  print 'win:lose = {}:{}'.format(win, lose)
