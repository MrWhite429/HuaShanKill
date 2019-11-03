import random
import player as pl
import cards as cd
import output as op
import pygame
from pygame.locals import *

class Model(pl.Player):
	img_path = "MengH"
	default_situation = ["孟获", 4, 0, "蜀"]

	def get_card(self):
		print(self.name, "的摸牌阶段")
		if (self.max_hp - self.hp <= 1):
			for i in range(0, 2):
				self.has_card.append(cd.get_new_card())
		else:
			print("%s发动技能【再起】获得了：" % (self.name))
			for i in range(self.max_hp - self.hp):
				tmp = cd.get_new_card()
				tmp.show()
				if (tmp.type == 1):
					print(" %s回复1点体力" % (self.name), end="")
					self.hp += 1
				else:
					self.has_card.append(tmp)
				print()

	def be_aimed(self, now_card, user):
		if (now_card == 0):
			return 1
		if (now_card.id == 12):
			print("%s发动技能【祸首】" % (self.name))
			return 0
		if (now_card.id == 13):
			return self.hp < self.max_hp
		elif (now_card.id == 16):
			return self.equip[0].id != 0
		elif (now_card.id in [8, 9, 10]):
			return len(self.has_card)
		elif (now_card.id in [11, 12]):
			return self.equip[1].id != 34
		return 1