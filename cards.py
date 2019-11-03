import random
import player as pl
import output as op



tck_card_nm = ["", "杀", "火杀", "雷杀", "闪", "桃",
			   "酒", "决斗", "火攻", "过河拆桥", "顺手牵羊",
			   "万箭齐发", "南蛮入侵", "桃园结义", "五谷丰登", "无中生有",
			   "借刀杀人", "铁索连环", "无懈可击", "乐不思蜀", "兵粮寸断",
			   "闪电", "诸葛连弩", "雌雄双股剑", "寒冰剑", "青虹剑",
			   "丈八蛇矛", "贯石斧", "麒麟弓", "朱雀羽扇", "青龙偃月刀",
			   "方天画戟", "八卦阵", "仁王盾", "藤甲", "白银狮子",
			   "绝影+1", "的卢+1", "爪黄飞电+1", "赤兔-1", "大宛-1",
			   "紫骍-1", "木牛流马"]

card_nm = ["", "杀", "火杀", "雷杀", "闪", "桃",							#01 - 05
		   "酒", "决斗", "火攻", "过河拆桥", "顺手牵羊",					#06 - 10
		   "万箭齐发", "南蛮入侵", "桃园结义", "五谷丰登", "无中生有",	#11 - 15
		   "借刀杀人", "铁索连环", "无懈可击", "乐不思蜀", "兵粮寸断",	#16 - 20
		   "闪电", "诸葛连弩", "雌雄双股剑", "寒冰剑", "青虹剑",			#21 - 25
		   "丈八蛇矛", "贯石斧", "麒麟弓", "朱雀羽扇", "青龙偃月刀",		#26 - 30
		   "方天画戟", "八卦阵", "仁王盾", "藤甲", "白银狮子",			#31 - 35
		   "绝影", "的卢", "爪黄飞电", "赤兔", "大宛",					#36 - 40
		   "紫骍", "木牛流马"]											#41 - 42

card_type = ["♠", "♥", "♣", "♦"]

card_point = ['', 'A ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10', 'J ', 'Q ', 'K ']

card_hp_num = [
	[1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 12, 12, 12, 13, 13],
	[1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 12, 13, 13],
	[1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 12, 12, 12, 13, 13],
	[1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 9, 10, 10, 11, 11, 12, 12, 12, 13, 13]]

card_hp_id = [
	[7, 21, 24, 32, 23, 10, 9, 10, 9, 36, 30, 19, 25, 3, 1, 12, 3, 1, 1, 6, 1, 1, 1, 1, 20, 18, 10, 26, 17, 9, 12, 40],
	[13, 11, 8, 4, 4, 5, 14, 2, 5, 14, 39, 28, 19, 5, 5, 15, 5, 15, 5, 15, 1, 1, 1, 15, 9, 5, 21, 38, 4],
	[35, 7, 22, 34, 1, 33, 32, 9, 1, 1, 9, 1, 37, 19, 3, 1, 1, 12, 3, 1, 1, 6, 1, 1, 20, 1, 1, 1, 1, 17, 16, 18, 18,
	 16],
	[29, 22, 7, 4, 4, 10, 4, 2, 4, 10, 42, 2, 4, 27, 4, 1, 1, 4, 1, 4, 6, 1, 4, 4, 1, 4, 4, 5, 31, 18, 1, 41]]

def_lvl = [99, 3, 3, 3, 0, 0,
		   0, 5, 5, 5, 5,
		   5, 5, 5, 6, 4,
		   5, 5, 3, 4, 4,
		   6, 2, 2, 2, 2,
		   2, 2, 2, 2, 2,
		   2, 1, 1, 4, 3,
		   2, 2, 2, 2, 2,
		   2, 3]

atk_lvl = [99, 3, 3, 3, 99, 1,
		   2, 5, 4, 2, 2,
		   2, 2, 5, 5, 1,
		   4, 2, 99, 2, 2,
		   99, 2, 2, 2, 2,
		   2, 2, 2, 2, 2,
		   2, 2, 2, 6, 4,
		   2, 2, 2, 2, 2,
		   2, 3]

danger_lvl = {0: 99, 22: 3, 23: 6, 24: 5, 25: 2,
			  26: 4, 27: 2, 28: 5, 29: 5, 30: 4,
			  31: 6, 32: 1, 33: 1, 34: 4, 35: 98,
			  36: 3, 37: 3, 38: 3, 39: 7, 40: 7,
			  41: 7, 42: 98}

throw_queue = []


class Card():
	def __init__(self, id, type, num, range):
		self.id = id			#名称
		self.type = type		#花色
		self.num = num			#点数
		self.range = range		#范围
		self.defence_level = def_lvl[self.id]		#（弃牌等）保留顺序
		self.attack_level = atk_lvl[self.id]		#（出牌等）打出顺序
		self.alpha = 1005  # 显示透明度

	def show(self):
		# print("%c" % (self.type + 3), end="")
		# print(self.num,self.id)
		# print("%s %s" % (card_point[self.num], card_nm[self.id]), end="")

		print(card_type[self.type],card_point[self.num],end="")
		print(card_nm[self.id],end="")

	def std_output(self, x, y, sx, sy):
		if(op.speedup_time>4):return
		tmp = op.card_img[self.id]
		tmp = op.scale(tmp, sx, sy)
		tmp.set_alpha(min(self.alpha, 255))
		op.screen.blit(tmp, [x, y])


# op.Stwrite(card_nm[self.id],x+18,y+2,16)


def aim(now_card, user, aimer):
	if (now_card == 0):
		return 0
	tot = len(pl.player_in_game)
	if (now_card.id == 10 or now_card.id == 20):
		# print(user.pos,aimer.pos)
		# now_card.show()
		return pl.distance(user, aimer) <= 1 and user.pos != aimer.pos
	elif (now_card.id <= 3):
		defence = aimer.equip[1]
		if (user.equip[0].id != 25):
			if (defence.id == 33 and now_card.type & 1 == 0):  # 仁王盾
				# print("%s使用了[%s]" % (aimer.name, card_nm[aimer.equip[1].id]))
				return 0
			elif (defence.id == 34 and now_card.id == 1):  # 藤甲
				# print("%s使用了[%s]" % (aimer.name, card_nm[aimer.equip[1].id]))
				return 0
		return pl.distance(user, aimer) <= user.equip[0].range and user.pos != aimer.pos
	elif (now_card.id in [5, 6, 15] or now_card.id > 20):
		return user.pos == aimer.pos
	elif (now_card.id in [4, 18, 11, 12, 13, 14]):
		return 0
	elif (now_card.id in [7, 9, 10, 16, 19]):
		return user.pos != aimer.pos

	return 1


card_heap = []


def _in(x, y, z, r):
	tmp = Card(x, y, z, r)
	tmp.alpha = 255
	card_heap.append(tmp)


def init():
	dic = {22: 1, 23: 2, 24: 2, 25: 2, 26: 3, 27: 3, 28: 5, 29: 4, 30: 3, 31:4}
	for i in range(0, 4):
		for j in range(0, len(card_hp_id[i])):
			id = card_hp_id[i][j]
			if (id > 21 and id < 32):
				_in(card_hp_id[i][j], i, card_hp_num[i][j], dic[id])
			else:
				_in(card_hp_id[i][j], i, card_hp_num[i][j], 0)
	random.shuffle(card_heap)


def get_new_card():
	if (len(card_heap)):
		tmp = card_heap[0]
		card_heap.pop(0)
		# tmp.show()
		return tmp
	else:
		init()
		return get_new_card()


def aiming(now_card: Card, user: pl.Player):
	pos = user.pos
	nid = now_card.id
	if (nid in [1, 2, 3, 7, 8, 9, 10, 16, 17, 18, 19, 20]):
		tmp = []
		for item in pl.player_in_game:
			if (item.pos == user.pos or item.dead or item.country == user.country):
				continue
			if aim(now_card, user, item) and item.be_aimed(now_card, user):
				tmp.append(item)
		if (len(tmp)):
			tmp.sort(key=lambda x:x.fire_col)
			num = 0
			if(len(tmp)>1):
				num = random.randint(0,1)		#容错（不能太专一）
			return tmp[num]
		return 0
	return user


def aiming_list(now_card: Card, user: pl.Player):
	pos = user.pos
	nid = now_card.id
	if (nid in [1, 2, 3, 7, 8, 9, 10, 16, 17, 18, 19, 20]):
		tmp = []
		for item in pl.player_in_game:
			if (item.pos == user.pos or item.dead):
				continue
			if aim(now_card, user, item) and item.be_aimed(now_card, user):
				tmp.append(item)
		if (len(tmp)):
			return tmp
		return 0
	return user


def use(now_card: Card, user, aimer, defence=1):
	tot = len(pl.player_in_game)
	x = user.pos
	y = aimer.pos
	nid = now_card.id
	throw_queue.append(now_card)
	op.use_card_arrow(user.seat, aimer.seat)
	pl.cd_score[x] += 1
	pl.upload([2,user,aimer,now_card])		#结算前视为指定目标
	if (nid in [1, 2, 3, 7, 8, 9, 10, 16, 17, 18, 19, 20]):
		if (pl.player_in_game[y].be_used(now_card, user) == 0):
			pl.upload([3, user, aimer, now_card])
			return
		# op.use_card_arrow(x, y)
		if (nid > 0 and nid < 4):
			st = user.skill[nid - 1]
			print("对%s使出一招“%s”，" % (aimer.name, st))
			if (user.gender != aimer.gender and user.equip[0].id == 23):
				print("%s使用了[%s]" % (user.name, card_nm[user.equip[0].id]))
				if(aimer.auto):
					if (len(aimer.has_card) > 2):
						tmp = pl.player_in_game[y].has_card.pop()
						print("%s丢掉了" % (aimer.name), end="")
						tmp.show()
						throw_queue.append(tmp)
					else:
						tmp = get_new_card()
						print("%s得到了" % (user.name), end="")
						tmp.show()
						pl.player_in_game[x].has_card.append(tmp)
				else:
					x = op.judge(("如何响应%s的%s?"%(user.name,card_nm[23])),380,30,["弃置一张牌","给对方一张牌"],420,30,0)
					if(x != 0):
						tmp = get_new_card()
						print("%s得到了" % (user.name), end="")
						tmp.show()
						pl.player_in_game[x].has_card.append(tmp)
					else:
						aimer.can_choose = 1
						x = 1
						while(sum(aimer.chosen)<1 or x!=0):
							op.choices_num = [0]*120
							x = op.judge("请弃置1张牌",380,30,["确定"],420,30,0)
						for i in range(len(aimer.chosen)):
							if(aimer.chosen[i] == 1):
								tmp = pl.player_in_game[y].has_card.pop(i)
								print("%s丢掉了" % (aimer.name), end="")
								tmp.show()
								throw_queue.append(tmp)
								break

			added = pl.player_in_game[x].drink
			in_lost = 0
			if (defence == 0):
				added += (aimer.equip[1].id == 34 and nid == 2)
				in_lost = added + 1
			elif (pl.player_in_game[y].need(4, user) == 0):
				added += (aimer.equip[1].id == 34 and nid == 2)
				in_lost = added + 1
			else:
				if (pl.player_in_game[x].be_defenced()):
					added += (aimer.equip[1].id == 34 and nid == 2)
					in_lost = added + 1
			if (in_lost):
				if (user.equip[0].id == 24 and len(aimer.has_card) > 1):
					x = 0
					if(user.auto == 0):
						op.choices_num = [0] * 120
						x = op.judge(("是否使用%s?"%(card_nm[24])), 380, 30, ["使用","不使用"], 420, 30, 0)
						op.has_end, op.has_confirm, op.has_cancel = 0, 0, 0
						op.task_queue.clear()
						op.task_queue.append(op.Button("结束出牌", 750, 400, 30, op.end_stage))
						op.task_queue.append(op.Button("确定", 460, 400, 30, op.confirm))
						op.task_queue.append(op.Button("取消", 590, 400, 30, op.cancel))
					if(x == 0):
						print("%s使用了[%s]" % (user.name, card_nm[user.equip[0].id]))
						for _ in range(2):
							dan_max, dan_pos = 95, -1
							for i in range(0, 5):
								if (danger_lvl[aimer.equip[i].id] < dan_max):
									dan_max = danger_lvl[aimer.equip[i].id]
									dan_pos = i
							if (dan_pos >= 0):
								tmp_card = pl.player_in_game[y].equip[dan_pos]
								print("丢弃了%s的" % (aimer.name), end="")
								tmp_card.show()
								print(",")
								if (tmp_card.id == 35):
									if (pl.player_in_game[y].hp < pl.player_in_game[y].max_hp):
										print("丢掉了[%s]并回复1点体力" % (card_nm[35]))
										pl.player_in_game[y].hp += 1
								pl.player_in_game[y].equip[dan_pos] = Card(0, 0, 0, dan_pos == 0)
								continue
							tmp = random.randint(0, len(aimer.has_card) - 1)
							tmp_card = aimer.has_card[tmp]
							print("丢弃了%s的" % (aimer.name), end="")
							tmp_card.show()
							print(",")
							throw_queue.append(tmp_card)
							# op.play(user)
							pl.player_in_game[y].has_card.pop(tmp)
					else:
						pl.player_in_game[y].lost_hp(in_lost, user,now_card.id - 1)
				else:
					if (user.equip[0].id == 28):
						print("%s使用了[%s]" % (user.name, card_nm[user.equip[0].id]))
						if (aimer.equip[2].id != 0):
							print("丢弃了%s的" % (aimer.name), end="")
							aimer.equip[2].show()
							pl.player_in_game[y].equip[2] = Card(0, 0, 0, 0)
						elif (aimer.equip[3].id != 0):
							print("丢弃了%s的" % (aimer.name), end="")
							aimer.equip[3].show()
							pl.player_in_game[y].equip[3] = Card(0, 0, 0, 0)
					pl.player_in_game[y].lost_hp(in_lost, user,now_card.id - 1)
			pl.upload([3, user, aimer, now_card])
			return
		print("对%s使出了一记“%s”，" % (aimer.name, card_nm[now_card.id]))
		if (nid == 7):
			if (defence == 1 and pl.player_in_game[y].need(18, user) != 0):
				pl.upload([3, user, aimer, now_card])
				return
			if (pl.player_in_game[y].multi_need([1, 2, 3]) == 0):
				pl.player_in_game[y].lost_hp(1, user)
			else:
				use(now_card, aimer, user, 0)

		elif (nid == 8):
			if (defence == 1 and pl.player_in_game[y].need(18, user) != 0):
				return
			if (len(aimer.has_card) <= 0): return
			tmp_n = 0
			if(len(aimer.has_card)>1):
				tmp_n = random.randint(0, len(aimer.has_card) - 1)
			print(tmp_n, len(aimer.has_card))
			tmp_card = aimer.has_card[tmp_n]
			print("%s 亮出了 " % (aimer.name), end="")
			tmp_card.show()
			print(",")
			for i in range(0, len(user.has_card)):
				if (user.has_card[i].type == tmp_card.type):
					print("%s接了" % (user.name), end=" ")
					user.has_card[i].show()
					print(",")
					pl.player_in_game[x].has_card.pop(i)
					added = (aimer.equip[1].id == 34)
					pl.player_in_game[y].lost_hp(added + 1, user,1)
					break
		elif (nid == 9):
			if (defence == 1 and pl.player_in_game[y].need(18, user) != 0):
				return
			dan_max, dan_pos = 95, -1
			for i in range(0, 5):
				if (danger_lvl[aimer.equip[i].id] < dan_max):
					dan_max = danger_lvl[aimer.equip[i].id]
					dan_pos = i
			if (dan_pos >= 0):
				tmp_card = pl.player_in_game[y].equip[dan_pos]
				print("丢弃了%s的" % (aimer.name), end="")
				tmp_card.show()
				print(",")
				if (tmp_card.id == 35):
					if (pl.player_in_game[y].hp < pl.player_in_game[y].max_hp):
						print("丢掉了[%s]并回复1点体力" % (card_nm[35]))
						pl.player_in_game[y].hp += 1
				throw_queue.append(tmp_card)
				pl.player_in_game[y].equip[dan_pos] = Card(0, 0, 0, dan_pos == 0)
				pl.upload([3, user, aimer, now_card])
				return
			if(len(aimer.has_card)<=0):return
			tmp_n = 0
			if (len(aimer.has_card) > 1):
				tmp_n = random.randint(0, len(aimer.has_card) - 1)
			print(tmp_n,len(aimer.has_card))
			tmp_card = aimer.has_card[tmp_n]
			throw_queue.append(tmp_card)
			print("丢弃了%s的" % (aimer.name), end="")
			tmp_card.show()
			print(",")
			pl.player_in_game[y].has_card.pop(tmp_n)
		elif (nid == 10):
			if (defence == 1 and pl.player_in_game[y].need(18, user) != 0):
				pl.upload([3, user, aimer, now_card])
				return
			dan_max, dan_pos = 95, -1
			for i in range(0, 5):
				if (danger_lvl[aimer.equip[i].id] < dan_max):
					dan_max = danger_lvl[aimer.equip[i].id]
					dan_pos = i
			if (dan_pos >= 0):
				tmp_card = pl.player_in_game[y].equip[dan_pos]
				print("得到了%s的" % (aimer.name), end="")
				tmp_card.show()
				print(",")
				if (tmp_card.id == 35):
					if (pl.player_in_game[y].hp < pl.player_in_game[y].max_hp):
						print("丢掉了[%s]并回复1点体力" % (card_nm[35]))
						pl.player_in_game[y].hp += 1
				pl.player_in_game[y].equip[dan_pos] = Card(0, 0, 0, dan_pos == 0)
				pl.player_in_game[x].has_card.append(tmp_card)
				pl.upload([3, user, aimer, now_card])
				return
			if (len(aimer.has_card) <= 0): return
			tmp_n = random.randint(0, len(aimer.has_card) - 1)
			print(tmp_n, len(aimer.has_card))
			tmp_card = aimer.has_card[tmp_n]
			print("得到了%s的" % (aimer.name), end="")
			tmp_card.show()
			print(",")
			pl.player_in_game[x].has_card.append(tmp_card)
			pl.player_in_game[y].has_card.pop(tmp_n)
		elif (nid == 16):
			if (defence == 1 and pl.player_in_game[y].need(18, user) != 0):
				pl.upload([3, user, aimer, now_card])
				return
			used = pl.player_in_game[y].multi_need([1, 2, 3])
			if (used != 0):
				new_aimer = aiming(used, aimer)
				if (new_aimer != 0):
					use(used, aimer, new_aimer)
					pl.upload([3, user, aimer, now_card])
					return
			pl.player_in_game[x].has_card.append(pl.player_in_game[y].equip[0])
			print("得到了%s的" % (aimer.name))
			pl.player_in_game[y].equip[0].show()
			pl.player_in_game[y].equip[0] = Card(0, 0, 0, 1)
		elif (nid == 17):
			if(aimer.connect == 0):
				print("横置了%s" % (aimer.name))
			else:
				print("解除了%s的横置" % (aimer.name))
			aimer.connect ^= 1
		elif (nid == 19):
			pl.player_in_game[y].judge.append(now_card)
		elif (nid == 20):
			pl.player_in_game[y].judge.append(now_card)

	elif (nid > 21):

		if (nid > 21 and nid < 32):
			print("拾起了%s," % (card_nm[now_card.id]))
			if (pl.player_in_game[x].equip[0].id != 0):
				pl.player_in_game[x].equip[0].alpha = 255
				throw_queue.append(pl.player_in_game[x].equip[0])
			pl.player_in_game[x].equip[0] = now_card
		elif (nid > 31 and nid < 36):
			print("装上了%s," % (card_nm[now_card.id]))
			if (pl.player_in_game[x].equip[1].id == 35):
				if (pl.player_in_game[x].hp < pl.player_in_game[x].max_hp):
					print("丢掉了[%s]并回复1点体力" % (card_nm[35]))
					pl.player_in_game[x].hp += 1
			if (pl.player_in_game[x].equip[1].id != 0):
				pl.player_in_game[x].equip[1].alpha = 255
				throw_queue.append(pl.player_in_game[x].equip[1])
			pl.player_in_game[x].equip[1] = now_card
		elif (nid > 35 and nid < 39):
			if (pl.player_in_game[x].equip[2].id != 0):
				pl.player_in_game[x].equip[2].alpha = 255
				throw_queue.append(pl.player_in_game[x].equip[2])
			print("骑上了%s," % (card_nm[now_card.id]))
			pl.player_in_game[x].equip[2] = now_card
		elif (nid > 38 and nid < 42):
			if (pl.player_in_game[x].equip[3].id != 0):
				pl.player_in_game[x].equip[3].alpha = 255
				throw_queue.append(pl.player_in_game[x].equip[3])
			print("骑上了%s," % (card_nm[now_card.id]))
			pl.player_in_game[x].equip[3] = now_card
		elif (nid == 42):
			if (pl.player_in_game[x].equip[4].id != 0):
				pl.player_in_game[x].equip[4].alpha = 255
				throw_queue.append(pl.player_in_game[x].equip[4])
			print("发现了%s," % (card_nm[now_card.id]))
			pl.player_in_game[x].equip[4] = now_card

	else:

		if (nid == 5):
			if (pl.player_in_game[y].be_used(now_card, user) == 0):
				pl.upload([3, user, aimer, now_card])
				return
			print("吃了口“%s”," % (card_nm[now_card.id]))
			pl.player_in_game[x].hp += 1
			return
		elif (nid == 6):
			if (pl.player_in_game[y].be_used(now_card, user) == 0):
				pl.upload([3, user, aimer, now_card])
				return
			print("喝了口“%s”," % (card_nm[now_card.id]))
			pl.player_in_game[x].drink = 1
			return
		elif (nid == 15):
			if (pl.player_in_game[y].be_used(now_card, user) == 0):
				pl.upload([3, user, aimer, now_card])
				return
			print("以内功“%s”," % (card_nm[now_card.id]))
			pl.player_in_game[x].has_card.append(get_new_card())
			pl.player_in_game[x].has_card.append(get_new_card())
		# elif (nid == 17):
		# 	if (pl.player_in_game[y].be_used(now_card, user) == 0):
		# 		pl.upload([3, user, aimer, now_card])
		# 		return
		# 	print("重铸了“%s”," % (card_nm[now_card.id]))
		# 	pl.player_in_game[x].has_card.append(get_new_card())
		else:
			print("%s趁众人不备，用出了“%s”," % (user.name, card_nm[now_card.id]))
			if (nid == 11):
				for item in pl.player_in_game:
					if (item.dead or item.pos == x or item.be_aimed(now_card, user) == 0):
						continue
					if (defence == 1 and pl.player_in_game[item.pos].need(18, user) != 0):
						continue
					if (pl.player_in_game[item.pos].be_used(now_card, user) == 0):
						continue
					op.use_card_arrow(x, item.seat)
					if (pl.player_in_game[item.pos].need(4, user) == 0):
						pl.player_in_game[item.pos].lost_hp(1, user)

			elif (nid == 12):
				for item in pl.player_in_game:
					if (item.dead or item.pos == x or item.be_aimed(now_card, user) == 0):
						continue
					if (defence == 1 and pl.player_in_game[item.pos].need(18, user) != 0):
						continue
					if (pl.player_in_game[item.pos].be_used(now_card, user) == 0):
						continue
					op.use_card_arrow(x, item.seat)
					if (pl.player_in_game[item.pos].multi_need([1, 2, 3]) == 0):
						pl.player_in_game[item.pos].lost_hp(1, user)

			elif (nid == 13):
				for item in pl.player_in_game:
					y = item.pos
					if (pl.player_in_game[item.pos].be_used(now_card, user) == 0):
						continue
					op.use_card_arrow(x, item.seat)
					if (item.dead == 0 and item.be_aimed(now_card, user)):
						pl.player_in_game[y].hp += 1

			elif (nid == 14):
				tmp_card_list = []
				for item in pl.player_in_game:
					if(item.dead == 0):
						tmp_card_list.append(get_new_card())
				tmp_card_list.sort(key= lambda x:x.defence_level)
				for item in tmp_card_list:
					print(card_nm[item.id])
				for item in pl.player_in_game:
					y = item.pos
					if (item.dead == 1 or pl.player_in_game[item.pos].be_used(now_card, user) == 0):
						continue
					op.use_card_arrow(x, item.seat)
					if (item.be_aimed(now_card, user)):
						tmp_card = tmp_card_list.pop(0)
						print("%s拿到了%s，" % (item.name, card_nm[tmp_card.id]))
						pl.player_in_game[y].has_card.append(tmp_card)
			print()
	pl.upload([3, user, aimer, now_card])
# print("%s观望四周" % (user.name), end="")
