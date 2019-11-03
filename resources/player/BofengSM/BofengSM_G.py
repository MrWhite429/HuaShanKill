import cards as cd
import player as pl
import output as op
import gamer as gm
import pygame
from pygame.locals import *
import random

class Model(gm.Gamer):
	img_path = "BofengSM"

	mark_pos = [0] * 120
	skill_used = 0

	def self_output(self,x,y):
		tot = len(pl.player_in_game)
		for i in range(1, tot + 1):
			tx = (i - (i > pl.gamer_pos and pl.gamer_pos != -1)) * 1000 / (tot + (pl.gamer_pos == -1))
			ty = max(130, 0.001 * tx * tx - 1 * tx + 350)
			tx -= 60
			ty -= 80
			for item in pl.player_in_game:
				if (item.seat == i - 1 and item.pos != self.pos):
					op.write("飞雷神×"+str(0+self.mark_pos[item.pos]),tx+95,ty+170,20,[200,200,0])
		op.write("距离-" + str(0 + max(self.mark_pos)), x +100 , y-60, 25, [200, 150, 50])



	skill_name = [("印记", 1, 0), ("瞬身", 1, 0)]

	def response(self, evt):
		if(evt == [1,self,3,0]):
			if(len(self.has_card)<1):return
			x = -1
			while (x == -1):
				op.choices_num = [0] * 120
				x = op.judge(("是否发动技能【印记】?"), 360, 30, ["确定", "取消"], 400, 30, 0)
			if(x == 1):return
			x = -1
			self.pl_can_choose = 1
			self.can_choose = 1
			while (x == -1 or sum(self.pl_chosen) < 1 or sum(self.chosen) < 1):
				op.choices_num = [0] * 120
				x = op.judge(("请选择一名其他角色并弃1张手牌发动【印记】"), 360, 30, ["确定"], 400, 30, 0)
			for i in range(len(self.has_card)):
				if(self.chosen[i] != 0):
					tmp = self.has_card.pop(i)
					cd.throw_queue.append(tmp)
					print("%s弃置了"%(self.name),end="")
					tmp.show()
					print()
					break
			self.chosen = [0]*120
			for i in range(len(pl.player_in_game)):
				if(self.pl_chosen[i] != 0):
					self.mark_pos[i] += 1
			self.attack_dis = max(self.mark_pos)

	def lost_hp(self,num,user,type = 0):
		if(self.mark_pos[user.pos]>0):
			x = -1
			while (x == -1):
				op.choices_num = [0] * 120
				x = op.judge(("是否发动技能【瞬身】减少飞雷神(%d)抵消此伤害?"%(self.mark_pos[user.pos])),
							 360, 30, ["确定", "取消"], 400, 30, 0)
			if(x == 0):
				print("%s发动技能【瞬身】抵消了伤害"%(self.name))
				self.mark_pos[user.pos] -= 1
				self.attack_dis = max(self.mark_pos)
				return 0
		if (self.equip[1].id == 35):
			if (num > 1):
				print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[1].id]))
				num = 1
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



