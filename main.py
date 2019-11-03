# -*- coding: utf-8 -*-
import cards as cd
import player as pl
import output as op
import gamer as gm
import room as rm
import threading


in_game = 0
game_end = 0


class check_cards(threading.Thread):
	def run(self):
		op.task_queue.clear()
		rm.init()
		while (rm.game_num<rm.all_num):
			rm.start()
		rm.show_result()
		global game_end
		game_end = 1
		return


if __name__ == "__main__":
	while(1):
		op.in_title = 1
		op.title()
		pl.import_pl()
		gm.import_pl()
		# op.edit()
		th = check_cards()
		op.init()
		th.start()
		game_end = 0
		while (game_end == 0):
			op.play(rm.now_player)
			op.act_check()
