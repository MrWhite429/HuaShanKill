import cards as cd
import player as pl
import output as op
import gamer as gm

room_max_seat = 14
all_num = 100
now_player = 0
game_num = 0


def add():
	pl.player_in_game = []
	# pl.player_in_game.append(gm.scripts["ZhangRZ"]("张睿之", 10, 0, "神"))
	pl.player_in_game.append(gm.scripts["SunC"]("孙策", 4, 0, "吴"))
	pl.player_in_game[0].has_card.append(cd.Card(17,0,12,1))
	pl.player_in_game[0].has_card.append(cd.Card(2, 0, 12, 1))
	pl.player_in_game[0].has_card.append(cd.Card(6, 3, 9, 1))
	pl.player_in_game.append(pl.scripts["WangYP"](("王宇鹏", 3, 0, "魏")))
	pl.player_in_game.append(pl.scripts["TaoSZ"](("陶思哲", 4, 0, "魏")))
	# pl.player_in_game.append(pl.scripts["HuaT"]("王重阳", 5, 0, "蜀"))
	# pl.player_in_game.append(pl.scripts["Shen_ZhaoY"]("神赵云", 2, 0, "吴"))
	# pl.player_in_game.append(pl.scripts["MengH"]("孟获5", 4, 0, "吴"))
	# pl.player_in_game.append(pl.scripts["SP_ZhaoY"]("ＳＰ赵云", 3, 0, "群"))
	# pl.player_in_game.append(pl.scripts["YuzhiboY"]("宇智波鼬", 3, 0, "吴"))

	# pl.player_in_game.append(pl.scripts["HuaT"]("华佗", 3, 0, "群"))
	# pl.player_in_game.append(pl.scripts["ZhaoYB"]("赵艺博", 4, 0, "魏"))
	pl.player_in_game.append(pl.scripts["HeYW"](("何雨葳", 3, 0, "吴")))
	pl.player_in_game[3].has_card = []
	pl.player_in_game[3].equip[1] = cd.Card(34,1,1,1)
	# pl.player_in_game.append(pl.scripts["YuZJ"]("于泽嘉", 4, 0, "魏"))
	# pl.player_in_game.append(pl.scripts["WangZY"]("王泽宇", 3, 0, "魏"))
	# pl.player_in_game.append(pl.scripts["WangSB"]("王三宝", 3, 0, "魏"))


def init():
	add()
	for item in pl.player_in_game:
		pl.country_score[item.country] = 0

def start():
	global game_num
	add()
	pl.init()
	while(pl.game_over() == 0):
		for item in pl.player_in_game:
			global now_player
			now_player = item
			if (item.dead == 1): continue
			item.wave()
			if (pl.game_over()):
				if (pl.gamer_pos != -1):
					pl.player_in_game[pl.gamer_pos].get_in = [0, 0, 0, 0, 0, 0]
				in_game = 0
				for i in range(len(pl.player_in_game)):
					tmp = pl.player_in_game[i]
					if (tmp.dead == 0):
						pl.score[tmp.pos] += 1
				for i in range(len(pl.player_in_game)):
					tmp = pl.player_in_game[i]
					if (tmp.dead == 0):
						pl.country_score[tmp.country] += 1
						break
				game_num += 1
				print("waaaa %d aaaaa" % (game_num))
				for item in pl.player_in_game:
					print(item.name, pl.score[item.pos])
				break



def show_result():
	print("势力\t胜场\t\t胜率(%)")
	for it in pl.country_score:
		print("%s\t (%3.d/%4.d)\t\t%lf" % (it,
										   pl.country_score[it],
										   all_num,
										   100 * pl.country_score[it] / all_num))
	print()
	print("势力 名称\t\t  胜场\t\t   胜率(%)\t\t平均出牌数\t\t平均回合数")
	for item in pl.player_in_game:
		pl.waves_score[item.pos] = max(pl.waves_score[item.pos], 1)
		print("%s\t%s\t (%3.d/%4.d)\t\t%lf\t\t%lf\t\t%lf" % (item.country, item.name,
															 pl.score[item.pos],
															 all_num,
															 100 * pl.score[item.pos] / all_num,
															 pl.cd_score[item.pos] / pl.waves_score[item.pos],
															 pl.waves_score[item.pos] / all_num))