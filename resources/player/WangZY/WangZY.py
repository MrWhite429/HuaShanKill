import random
import player as pl
import cards as cd
import output as op
import pygame
from pygame.locals import *

class Model(pl.Player):
	# 【吟诵】：摸牌阶段，你可以放弃摸牌并将牌堆顶的牌放置于你的武将牌上，称为“音”。
	# 		当一张“音”与其他“音”花色相同时，你弃置该牌，并获得所有的“音”，且直到
	# 		本回合结束，你的“杀”可指定X名目标。（X为“音”的数量）
	# 【爽朗】：限定技，当你濒死时，你可以减少1点体力上限并恢复至2点体力。
	img_path = "WangZY"
	default_situation = ["王泽宇", 3, 0, "蜀"]
	limit = 1
	tot = 1

	def self_output(self, x, y):
		if (self.limit == 1):
			pygame.draw.rect(op.screen, [150, 0, 0], [x + 20, y, 20, 20], 0)
			op.write(" 限", x + 40, y + 1, 18, [255, 255, 255])

	def lost_hp(self, num, user, type = 0):
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
			if (self.limit == 1):
				print("%s发动技能【爽朗】" % (self.name))
				self.limit = 0
				self.hp = 2
				self.max_hp = 2
			else:
				self.died()
				return num
		pl.upload([4, user, num, self,type])
		return num

	def get_card(self):
		print("%s发动技能【吟诵】" % (self.name))
		used = []
		while (len(used) < 4):
			tmp = cd.get_new_card()
			print("判定结果为:", end="")
			tmp.show()
			print()
			if (tmp.type in used):
				break
			used.append(tmp.type)
			self.has_card.append(tmp)
		can_aimed = 0
		for item in pl.player_in_game:
			if (item.dead == 1 or item.pos == self.pos):
				continue
			can_aimed += 1
		tot = min(len(used), can_aimed)
		print("%s可指定%d个目标" % (self.name, tot))
		for i in range(max(0, 2 - tot)):
			self.has_card.append(cd.get_new_card())

	def event(self):
		print(self.name, "的出牌阶段")
		self.has_card.sort(key=lambda x: x.attack_level)
		for item in self.has_card:
			item.show()
			print()
		print()
		i = 0
		try_kill = 1
		while (i < len(self.has_card)):
			if (self.dead): return
			item = self.has_card[i]
			# print("in ",end="")
			# item.show()
			if (item.attack_level == 99):
				break
			if (len(self.has_card) > 2 and item.attack_level > 3 and i < len(self.has_card) - 1):
				if (self.equip[0].id == 26 and self.use_kill == 0 and try_kill):
					print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
					pop_card_1 = self.has_card.pop(i)
					pop_card_2 = self.has_card.pop(i)
					tmp = cd.Card(1, (pop_card_1.type % 2) ^ (pop_card_2.type % 2), 1, 1)
					aimer = cd.aiming(tmp, self)
					using_res, item = self.using(tmp)
					if (using_res and aimer != 0):
						pop_card_1.show()
						print()
						pop_card_2.show()
						print()
						cd.use(tmp, self, aimer)
					else:
						i = -1
						self.has_card.sort(key=lambda x: x.attack_level)
						self.has_card.append(pop_card_1)
						self.has_card.append(pop_card_1)
					try_kill = 0

			aimer = cd.aiming(item, self)
			using_res, item = self.using(item)
			if (using_res and aimer != 0):
				if (len(self.has_card) > i): self.has_card.pop(i)
				if (item.id < 4):
					kill_set = cd.aiming_list(item, self)
					i = 0
					if (kill_set != 0):
						while (i < min(len(kill_set), self.tot)):
							cd.use(item, self, kill_set[i])
							i += 1
					self.used(item)
				else:
					cd.use(item, self, aimer)
					self.used(item)
				i = -1
				self.has_card.sort(key=lambda x: x.attack_level)
			i += 1