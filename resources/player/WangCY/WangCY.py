import random
import player as pl
import cards as cd
import output as op
import pygame
from pygame.locals import *

class Model(pl.Player):
	#【尊上】：当你受到一名角色的伤害时，伤害来源需弃置一张基本牌，否则你可以防止此伤害。
	img_path = "WangCY"
	default_situation = ["王重阳", 3, 0, "魏"]

	def lost_hp(self, num, user,type= 0):
		print("%s发动技能【尊上】" % (self.name))
		if (len(pl.player_in_game[user.pos].has_card) < 2):
			return
		if (pl.player_in_game[user.pos].multi_need([1, 2, 3, 4, 5, 6]) == 0):
			return
		st = ["%s被掌力击退，向后直跌了%d步，", "%s中了一击，吐出%d口鲜血，", "%s眉头一皱，只知这一掌下去功力已失了%d成，"]
		tmp = st[random.randint(0, 2)]
		print(tmp % (self.name, num))
		self.hp -= num
		while (self.hp < 1):
			if (self.dying() == 0):
				break
			else:
				self.hp += 1
		if (self.hp < 1):
			self.died()
			return num
		pl.upload([4, user, num, self,type])
		return num
