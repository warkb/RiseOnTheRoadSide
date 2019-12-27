from time import time

class ShowLoad():
    """
    Этот модуль позволяет понять, 
    как много требуется времени на отрезок кода
    """
    def __init__(self):
        self.resetQueue()

    def resetQueue(self):
        self.queue = []
        self.startTime = time()

    def addTimePoint(self, name):
        """
        Добавляет точку в коде с именем name
        для которой будет отсчитываться время выполнения
        """
        self.queue.append((name, time()-self.startTime))

    def showLoad(self):
        """
        Возвращает объект вида
        {
            Имя точки отсчета
            Занимаемое время в процентах
        }
        """
        loadList = []
        fullTime = self.queue[-1][1] - self.queue[0][1]
        for i in range(len(self.queue) - 1):
            current = self.queue[i]
            nextEl = self.queue[i+1]
            loadList.append({
                "имя": current[0],
                "время": round(((nextEl[1] - current[1])/fullTime)*100)
                })
        return loadList
        