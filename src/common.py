#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import logging

class Characters:
  PRINCESS = 0
  KNIGHT = 1
  ORC = 2
  BOSS_ORC = 3

NAMES = {
  0: 'princess',
  1: 'knight',
  2: 'orc',
  3: 'boss-orc',
}

def name(ch):
  ''' コードに対応したカード名を取得します '''
  return NAMES[ch]

def id(x):
  return x

ACTION_ORDER_LIST = {
  'change': 1, # 配置転換
  'draw': 1, # 相打ち
  'ambush': 2, # 奇襲攻撃
  'pincer_attack': 2, # 挟み撃ち
  'disguise': 3, # 変装
  'copy': 3, # 写し身
  'charm': 4, # 魅了
  'revenge': 5, # 復讐
  'strong_violence': 5, # 数の暴力
}

def rand_ordered_action_list():
  '''
  ゲームの実行順序として有効なアクション順列を生成します
  '''
  actions = random.sample(ACTION_ORDER_LIST.keys(), 4)
  return sorted(actions, cmp=lambda a,b: ACTION_ORDER_LIST[a] - ACTION_ORDER_LIST[b]) 


def rand_field_seq():
  '''
  ランダムな回廊を生成します。
  ただし、姫は常に0の位置に居ます。
  ''' 
  seq = [Characters.BOSS_ORC] 
  seq = seq + ([Characters.KNIGHT] * 2)
  seq = seq + ([Characters.ORC] * 4)
  random.shuffle(seq)
  return [Characters.PRINCESS] + seq


class Game:
  ''' 1ゲームの場を表現するMutableなデータです '''
  def __init__(self, field=None, jail=None, played_card=None):
    self.field = rand_field_seq() if field is None else field
    self.jail = [] if jail is None else jail 
    self.played_card = [] if played_card is None else played_card

  def is_princess_win(self):
    ''' 姫が勝利しているか否かを返します ''' 
    return Characters.PRINCESS not in self.jail
  
  def update(self, action_name, action_func):
    ''' action(Game) を適用します '''
    action_func(self)
    self.played_card.append(action_name)
  
  def gotojail(self, index):
    ''' 現在のfieldのindex番目のキャラクターを牢屋に送ります '''
    length = len(self.field)
    if -length <= index < length:
      ch = self.field.pop(index)
      self.jail.append(ch)

  def __str__(self):
    return '\n'.join([
    '-------------------',
    'Current Winner: {}'.format('Princess' if self.is_princess_win() else 'Orcs'),
	  'Current Field: {}'.format(self.field),
	  'Current Jail: {}'.format(self.jail),
	  'Played Card: {}'.format(self.played_card),
    '-------------------',
	])


