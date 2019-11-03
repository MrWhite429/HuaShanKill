import random
import player as pl
import cards as cd
import output as op
import pygame
from pygame.locals import *

class Model(pl.Player):
	# 【解锁】：摸牌阶段开始时，你可以所有角色摸一张牌，每当有角色以此法获得一张牌时，你
	# 		摸一张牌。
	img_path = "WangSB"
	default_situation = ["王三宝", 3, 0, "吴"]

	def get_card(self):
		print(self.name, "的摸牌阶段")
		num = 2
		if (len(self.has_card) < self.max_hp + 2):
			print("%s发动技能【解锁】" % (self.name))
			for item in pl.player_in_game:
				y = item.pos
				if (self.pos == y or item.dead == 1):
					continue
				tmp = cd.get_new_card()
				print("%s获得了" % (item.name), end="")
				tmp.show()
				print()
				pl.player_in_game[y].has_card.append(tmp)
				num += 1
		for i in range(0, num):
			self.has_card.append(cd.get_new_card())