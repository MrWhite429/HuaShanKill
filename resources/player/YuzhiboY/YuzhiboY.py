import random
import player as pl
import cards as cd
import output as op
import pygame
from pygame.locals import *

class Model(pl.Player):
	#【分身】：当一名角色受到伤害时，若其与你势力相同，你可以摸X张牌。（X为其当前损失的体力值）
	#【天照】：当你对一名角色使用【杀】或【决斗】后，你可以对其造成1点伤害。
	img_path = "YuzhiboY"
	default_situation = ["宇智波鼬", 3, 0, "吴"]

	def response(self, evt):
		if (evt[0] == 8):
			print(self.name, "：深表同情")

		if (evt[0] == 4):
			if (evt[3].country == self.country):
				for i in range(evt[3].max_hp - evt[3].hp):
					print("%s发动技能【分身】获得了" % (self.name))
					tmp = cd.get_new_card()
					tmp.show()
					print()
					self.has_card.append(tmp)
		if (evt[0] == 3):
			if (evt[1].pos == self.pos and evt[3].id in [1, 2, 3, 7]):
				if (len(self.has_card) > 0):
					print("%s发动技能【天照】" % (self.name))
					pl.player_in_game[evt[2].pos].lost_hp(1, self)
