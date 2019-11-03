import random
import player as pl
import cards as cd
import output as op
import pygame
from pygame.locals import *

class Model(pl.Player):
	# 【抉择】：准备阶段，你可以从【肝题】和【摸鱼】中选择一项技能，若你选择的技能与之前
	# 		不同，你需要弃置一张手牌。
	# 【肝题】：出牌阶段，当你使用非延时性锦囊牌生效后，你可以摸一张牌。
	# 【摸鱼】：结束阶段开始时，你可以将自己翻面，然后恢复1点体力并摸1张牌。
	img_path = "HeYW"
	skill_type = 0  # 技能类别：1摸鱼/2肝题
	skill_name = ["", "【摸鱼】", "【肝题】"]
	default_situation = ["何雨葳", 3, 0, "蜀"]

	def self_output(self, x, y):
		if (self.skill_type == 1):
			pygame.draw.rect(op.screen, [150, 0, 0], [x + 20, y, 40, 20], 0)
			op.write("摸鱼", x + 60, y + 1, 18, [255, 255, 255])
		if (self.skill_type == 2):
			pygame.draw.rect(op.screen, [0, 0, 150], [x + 20, y, 40, 20], 0)
			op.write("肝题", x + 60, y + 1, 18, [255, 255, 255])

	def prepare(self):
		print(self.name, "的准备阶段")
		if (self.skill_type == 0):
			print("%s发动技能【抉择】" % (self.name))
			self.skill_type = 2
		elif (len(self.has_card) > 0):
			change = 0
			if (self.hp <= 1 and self.skill_type == 2):
				print("%s发动技能【抉择】" % (self.name))
				self.skill_type = 1
				change = 1
			elif (self.hp > 1 and self.skill_type == 1):
				print("%s发动技能【抉择】" % (self.name))
				self.skill_type = 2
				change = 1
			if (change):
				tmp = self.has_card.pop()
				print("%s弃置了" % (self.name), end="")
				tmp.show()
				print()
				print("%s转换技能为%s" % (self.name, self.skill_name[self.skill_type]))

	def used(self, now_card):
		if (now_card.id < 4):
			self.use_kill = 1
			self.drink = 0
		elif (now_card.id > 6 and now_card.id < 17 and self.skill_type == 2):
			print("%s发动技能%s获得了" % (self.name, self.skill_name[2]), end=" ")
			tmp = cd.get_new_card()
			tmp.show()
			print()
			self.has_card.append(tmp)
		return 1

	def end(self):
		if (self.skill_type == 1):
			print("%s发动技能%s获得了" % (self.name, self.skill_name[1]), end=" ")
			self.flip ^= 1
			self.hp = self.hp + 1
			tmp = cd.get_new_card()
			tmp.show()
			print()
			self.has_card.append(tmp)