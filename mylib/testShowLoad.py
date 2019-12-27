from time import sleep
from showload import ShowLoad

sl = ShowLoad()

for _ in range(100):
	sl.resetQueue()
	sl.addTimePoint("логика")
	# тут мы обрабатываем логику
	sleep(3)

	# тут мы выполняем отрисовку
	sl.addTimePoint("отрисовка")
	sleep(2)

	# показываем, кто болеше нагружает
	sl.addTimePoint("Всё")
	print(sl.showLoad())