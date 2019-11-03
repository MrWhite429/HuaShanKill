import random
import player as pl
import cards as cd
import output as op
import pygame
from pygame.locals import *

class Model(pl.Player):
	# 【神奇】：锁定技，每当你受到一点伤害时，你增加一点体力上限。
	# 【厚颜】：摸牌阶段，你可以摸X张牌，X为你体力上限与体力值的比(向下取整)且至多为4。弃牌阶段，你弃置与体力值数量相等的牌。
	img_path = "TaoSZ"
	default_situation = ["陶思哲", 4, 0, "魏"]
	has_skill = 0

	def lost_hp(self, num, user, type = 0):
		self.hp -= num
		while (self.hp < 1):
			if (self.dying() == 0):
				break
			else:
				self.hp += 1
		if (self.hp < 1):
			self.died()
			return num
		if (self.dead == 0):
			print("%s发动了技能【神奇】增加了%d点体力上限" % (self.name,num))
			self.max_hp += num
		pl.upload([4, user, num, self,type])
		return num

	def get_card(self):
		self.has_skill = 0
		print(self.name, "的摸牌阶段")
		if (self.max_hp > 2 * self.hp):
			print("%s发动了技能【厚颜】并摸了%d张牌" % (self.name, min(4, max(2, int(self.max_hp // self.hp)))))
			self.has_skill = min(4, max(2, int(self.max_hp // self.hp)))

		for i in range(0, min(4, max(2, int(self.max_hp // self.hp)))):
			self.has_card.append(cd.get_new_card())

	def throw(self, num):
		print(self.name, "的弃牌阶段")
		print("%s发动了技能【神奇】" % (self.name))
		if (self.has_skill != 0):
			print("%s发动了技能【厚颜】" % (self.name))
			num = min(len(self.has_card), self.hp)
		print("弃置", num, "张")
		self.has_card.sort(key=lambda x: x.defence_level)
		for i in range(0, num):
			cd.throw_queue.append(self.has_card.pop())
		# op.play(self)
		for item in self.has_card:
			item.show()
			print()