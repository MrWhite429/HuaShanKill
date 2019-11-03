import random
import player as pl
import cards as cd
import output as op
import pygame
from pygame.locals import *

class Model(pl.Player):
	# 【失聪】：锁定技，当一张以你为目标的牌生效前，你需要进行一次判定，若判定结果与该牌
	# 		颜色相同，则该牌对你无效。
	img_path = "WangYP"
	default_situation = ["王宇鹏", 3, 0, "魏"]

	def judge_skill(self, now_card):
		print("%s发动了技能【失聪】" % (self.name))
		tmp = cd.get_new_card()
		now_card.show()
		print(" 判定结果为:", end=" ")
		tmp.show()
		print()
		if (now_card.type % 2 == tmp.type % 2):
			print("%s无效" % (cd.card_nm[now_card.id]))
			return 0
		return 1

	def be_used(self, now_card, user):
		return self.judge_skill(now_card)