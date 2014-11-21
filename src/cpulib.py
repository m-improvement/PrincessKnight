#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
CPU実装に利用する汎用関数を提供します。
'''
import random
import logging

def get_random_index(xs, value, else_value=None, excludes_index=[]):
  '''
  xsの中の値がvalueであるindexをランダムに選んで返します。
  存在しない場合はelse_valueが返ります。
  また、結果として除外するindexがある場合、excludes_indexにそのindexを含めてください。
  '''
  if value not in xs:
    return else_value
  
  value_cnt = len(filter(lambda x: x == value, xs))
  ex_cnt = sum(map(lambda idx: 1 if xs[idx] == value else 0, excludes_index)) 
  if value_cnt == ex_cnt:
    # 存在しない
    return else_value

  maxvalue = len(xs) - 1
  while True:
    index = random.randint(0, maxvalue)
    if index not in excludes_index and xs[index] == value:
      return index


def get_adj_index(xs, index):
  '''
  xsに(index-1, index+1)でアクセス可能なインデックスの組を返します。
  0を下回った、あるいはlenを超えた場合は巡回します。
  '''
  left = index - 1
  right = (index + 1) % len(xs)
  return (left, right)


def get_adj(xs, index):
  '''
  (xs[index-1], xs[index+1]) を返します。
  0を下回った、あるいはlenを超えた場合は巡回します。
  '''
  (left, right) = get_adj_index(xs, index)
  return (xs[left], xs[right])



