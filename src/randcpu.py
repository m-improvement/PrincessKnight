#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
ランダムなストラテジーを提供します
'''
import random
import logging

import common
import cpulib


def change(g):
  '''
  配置転換戦略です
  '''
  logging.debug('Action: Change(1)')
  orc = cpulib.get_random_index(g.field, common.Characters.ORC)
  boss = cpulib.get_random_index(g.field, common.Characters.BOSS_ORC)
  if orc is None or boss is None:
    logging.debug('No Change due to There is No Target(s)')
    return g
  (g.field[orc], g.field[boss]) = (g.field[boss], g.field[orc])
  logging.debug('Swapped Orc({}) <=> Boss-Orc({})'.format(orc, boss))
  return g


def draw(g):
  ''' 相打ちの実装です '''
  logging.debug('Action: Draw(1)')

  def start_index():
    # ひとつシフトした内容とzipを取り、ランダムにシャッフルする
    shifted = g.field[1:] + g.field[:1]
    
    # (index, (left, right)) の構造
    zipped = zip(xrange(0, len(g.field)), zip(g.field, shifted))
    random.shuffle(zipped)
    
    for (index, (left, right)) in zipped:
      if left == common.Characters.ORC and right == common.Characters.KNIGHT:
        return index 
      if left == common.Characters.KNIGHT and right == common.Characters.ORC:
        return index
    return None

  left_index = start_index()
  if left_index == None:
    logging.debug('No Adjucency Knight and Orc!')
    return
  
  right_index = (left_index + 1) % len(g.field)

  left = g.field[left_index]
  right = g.field[right_index]

  # インデックスの大きい方から牢屋に入れる
  g.gotojail(max(left_index, right_index))
  g.gotojail(min(left_index, right_index))
  
  logging.debug('Goto Jail: {}({}) and {}({})'.format(
    common.name(left), left_index, common.name(right), right_index))
  return g


def ambush(g):
  ''' 奇襲の実装です '''
  logging.debug('Action: Ambush(2)')
  princess = cpulib.get_random_index(g.field, common.Characters.PRINCESS, -1)
  if princess == -1:
    logging.debug('Princess is already into Jail!')
    return g

  (left, right) = cpulib.get_adj_index(g.field, princess)
  rm_index = random.choice([left, right])
  ch = g.field[rm_index]
  g.gotojail(rm_index)
  logging.debug('Goto Jail: {}({})'.format(common.name(ch), rm_index))
  return g


def pincer_attack(g):
  ''' 挟み撃ちの実装です '''
  logging.debug('Action: Pincer Attack(2)')
  princess = cpulib.get_random_index(g.field, common.Characters.PRINCESS, -1)
  if princess == -1:
    logging.debug('Princess is already into Jail!')
    return g

  (left, right) = cpulib.get_adj(g.field, princess)
  if left == common.Characters.ORC and right == common.Characters.ORC:
    # 挟み撃ち成功(姫騎士を牢屋へ)
    g.gotojail(princess)
    logging.debug('Princess Goto Jail!')
  else:
    # 挟み撃ち失敗(ランダムにオークを牢屋へ)
    ork = cpulib.get_random_index(g.field, common.Characters.ORC)
    g.gotojail(ork)
    logging.debug('Ork Goto Jail({})'.format(ork))
  return g

def disguise(g):
  ''' 変装の実装です '''
  logging.debug('Action: Disguise(3)')
  knight = cpulib.get_random_index(g.field, common.Characters.KNIGHT)
  if knight == None:
    logging.debug('No Knight on Field!')
    return g

  princess = cpulib.get_random_index(g.field, common.Characters.PRINCESS)
  if princess == None:
    # 姫騎士は牢屋に居る
    g.jail.remove(common.Characters.PRINCESS)
    g.jail.append(common.Characters.KNIGHT)
    g.field[knight] = common.Characters.PRINCESS
    logging.debug('Princess JailBreaks! (Knight({}) goto jail)'.format(knight))
  else:
    # 姫騎士は回廊に居る
    (g.field[princess], g.field[knight]) = (g.field[knight], g.field[princess])
    logging.debug('Swap Princess({}) <=> Knight({})'.format(princess, knight))
  return g


def copy(g):
  ''' 写し身の実装です '''
  logging.debug('Action: Copy(3)')
  if len(g.played_card) == 0:
    logging.debug('No Card Played!')
    return g

  # 利用済みカードをランダムにチョイスして実行
  copy_name = random.choice(g.played_card)
  logging.debug('Copy: {}'.format(copy_name))
  strategy(g, copy_name)(g)
  logging.debug('Run Copied Action')
  return g

def charm(g):
  ''' 魅了の実装です '''
  logging.debug('Action: Charm(4)')
  if common.Characters.PRINCESS not in g.field:
    logging.debug('Princess is already in jail (No Charm)')
    return g
  if common.Characters.ORC not in g.jail:
    logging.debug('No Orc in Jail Now (No Charm)')
    return g
  # 姫の右隣に牢屋からオークを1体持ってくる
  princess = cpulib.get_random_index(g.field, common.Characters.PRINCESS)
  g.field.insert(princess + 1, common.Characters.ORC)
  g.jail.remove(common.Characters.ORC)
  logging.debug('Orc where was in jail appeared next Princess ({})!'.format(princess + 1)) 
  return g

def revenge(g):
  ''' 復讐の実装です '''
  logging.debug('Action: Revenge(5)')
  if 'strong_violence' in g.played_card:
    # 数の暴力を利用している場合には効果は無い
    logging.debug('No Effect due to Strong-Violence Action')
    return g
  
  boss = cpulib.get_random_index(g.field, common.Characters.BOSS_ORC)
  if boss == None:
    logging.debug('No Effect due to There is no Boss-Orc!')
    return g
  
  X = len(filter(lambda ch: ch == common.Characters.ORC, g.jail))
  logging.debug('{} characters goto jail'.format(X))

  if len(g.field) <= X:
    # 全て牢屋に入れる
    logging.debug('All Characters goto jail!')
    for i in xrange(0, len(g.field)):
      g.gotojail(0)
  else:
    # 牢屋に入れる内容をマークする
    jaillist = []
    for i in xrange(0, X):
      idx = boss - i - 1
      logging.debug('{}({}) goto jail'.format(common.name(g.field[idx]), idx))
      jaillist.append(g.field[idx])
      g.field[idx] = -1
    # まとめて牢屋に入れる
    g.field = filter(lambda x: x != -1, g.field)
    g.jail = g.jail + jaillist
  return g


def strong_violence(g):
  ''' 数の暴力の実装です '''
  logging.debug('Action: Strong-Violence(5)')
  if 'revenge' in g.played_card:
    # 数の暴力を利用している場合には効果は無い
    logging.debug('No Effect due to Revenge Action')
    return g
  
  princess = cpulib.get_random_index(g.field, common.Characters.PRINCESS)
  if princess is None:
    logging.debug('No Effect due to There is no Princess!')
    return g

  orc_count = len(filter(lambda ch: ch == common.Characters.ORC, g.field))
  if orc_count >= 4:
    # 数の暴力の条件を満たす
    logging.debug('Princess goto jail!')
    g.gotojail(princess)
  else:
    # 数の暴力の条件を満たさない
    logging.debug('No Effect due to Orc is fewer...')
  
  return g
 

ACTION_LIST = {
  'change': change,
  'draw': draw,
  'ambush': ambush,
  'pincer_attack': pincer_attack,
  'disguise': disguise,
  'copy': copy,
  'charm': charm,
  'revenge': revenge,
  'strong_violence': strong_violence,
}

def strategy(g, key):
  ''' このプログラムが取るカード毎の戦略を返します '''
  return ACTION_LIST[key]


if __name__ == '__main__':
  # insert mock and run tests
  import doctest
  doctest.testmod()

