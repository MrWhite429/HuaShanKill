import random
import player as pl
import cards as cd
import output as op
import pygame
from pygame.locals import *

class Model(pl.Player):
	img_path = "SP_ZhaoY"
	default_situation = ["ＳＰ赵云", 3, 0, "群"]

	def need(self, need_id, user):
		# print("需要",self.name,"出",cd.card_nm[need_id])
		op.delay(300)
		if (need_id == 4 and self.equip[1].id == 32 and user.equip[0].id != 25):
			print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[1].id]))
			tmp = cd.get_new_card()
			print("判定结果：", end=" ")
			tmp.show()
			print()
			if (tmp.type == 1 or tmp.type == 3):
				print("[%s]生效" % (cd.card_nm[self.equip[1].id]))
				tmp.id = 4
				return tmp
		if (need_id == 4):
			change = self.multi_need([1, 2, 3])
			if (change != 0):
				print("%s发动技能【龙胆】" % (self.name))
				if (len(user.has_card) > 0):
					print("%s发动技能【冲阵】并获得%s的一张手牌" % (self.name, user.name))
					tmp_card = user.has_card.pop(random.randint(0, len(user.has_card) - 1))
					self.has_card.append(tmp_card)
				return change
		for i in range(0, len(self.has_card)):
			if (self.has_card[i].id == need_id):
				if (need_id == 4):
					tmp = ["向后一躲，避开了这一招", "片刻之间已侧身避过", "忽的跳出，早避开这招"]
					st = tmp[random.randint(0, 2)]
					print("%s%s," % (self.name, st))
				elif (need_id == 18):
					st = "早就看出端倪，轻松化开"
					print("%s%s," % (self.name, st))
				elif (need_id in [1, 2, 3]):
					st = self.skill[need_id]
					print("%s接了一记“%s”" % (self.name, st))
				else:
					st = cd.card_nm[need_id]
					print("%s打出了%s" % (self.name, st))
				tmp = self.has_card.pop(i)
				cd.throw_queue.append(tmp)
				# op.play(self)
				return tmp
		return 0

	def event(self):
		print(self.name, "的出牌阶段")
		self.has_card.sort(key=lambda x: x.attack_level)
		for item in self.has_card:
			item.show()
			print()
		print()
		i = 0
		try_kill = 1

		for item_t in self.has_card:
			if (item_t.id == 4 and try_kill == 1):
				item = cd.Card(1, 1, 1, 1)
				aimer = cd.aiming(item, self)
				using_res, item = self.using(item)
				if (using_res and aimer != 0):
					self.has_card.remove(item_t)
					print("%s发动技能【龙胆】" % (self.name))
					if (len(aimer.has_card) >= 1):
						tmp_card = aimer.has_card.pop(0)
						self.has_card.append(tmp_card)
						print("%s发动技能【冲阵】并获得%s的一张手牌" % (self.name, aimer.name))
					if (self.equip[0].id == 31 and item.id < 4 and len(self.has_card) == 0):
						kill_set = cd.aiming_list(item, self)
						i = 0
						if (kill_set != 0):

							while (i < min(len(kill_set), 3)):
								print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
								cd.use(item, self, kill_set[i])
								i += 1
						self.used(item)
					else:
						cd.use(item, self, aimer)
						self.used(item)
					self.has_card.sort(key=lambda x: x.attack_level)
					try_kill = 0

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
				if (self.equip[0].id == 31 and item.id < 4 and len(self.has_card) == 0):
					kill_set = cd.aiming_list(item, self)
					i = 0
					if (kill_set != 0):
						while (i < min(len(kill_set), 3)):
							print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
							cd.use(item, self, kill_set[i])
							i += 1
					self.used(item)
				else:
					cd.use(item, self, aimer)
					self.used(item)
				i = -1
				self.has_card.sort(key=lambda x: x.attack_level)
			i += 1
			# op.play(self)
			op.delay(400)
		for item_t in self.has_card:
			if (item_t.id == 4 and try_kill == 1):
				item = cd.Card(1, 1, 1, 1)
				aimer = cd.aiming(item, self)
				using_res, item = self.using(item)
				if (using_res and aimer != 0):
					self.has_card.remove(item_t)
					print("%s发动技能【龙胆】" % (self.name))
					if (len(aimer.has_card) >= 1):
						tmp_card = aimer.has_card.pop(0)
						self.has_card.append(tmp_card)
						print("%s发动技能【冲阵】并获得%s的一张手牌" % (self.name, aimer.name))
					if (self.equip[0].id == 31 and item.id < 4 and len(self.has_card) == 0):
						kill_set = cd.aiming_list(item, self)
						i = 0
						if (kill_set != 0):
							while (i < min(len(kill_set), 3)):
								print("%s使用了[%s]" % (self.name, cd.card_nm[self.equip[0].id]))
								cd.use(item, self, kill_set[i])
								i += 1
						self.used(item)
					else:
						cd.use(item, self, aimer)
						self.used(item)
					self.has_card.sort(key=lambda x: x.attack_level)
					try_kill = 0