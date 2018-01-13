def getProbsOnCosts(*costs):
	"""
	Принимает массив цен на артефакты, возвращает массив вероятностей
	их появления с учетом того, что цена обратно пропорциональна вероятности
	появления."""
	devider = 1
	for i in range(1, len(costs)):
		devider += costs[0] / costs[i]
	probs = [1 / devider]
	for i in range(1, len(costs)):
		probs.append(probs[0] * costs[0] / costs[i])
	return probs

artefactsType = {}
artefactsType['redball'] = {'color': 'EC0000', 'price':5000, 'prob': 0.125}
artefactsType['blueball'] = {'color': '0246C3', 'price':2500, 'prob': 0.25}
artefactsType['grayball'] = {'color': 'D8C6C6', 'price':1000, 'prob': 0.625}

#параметры экрана
WIDTHSCREEN = 1024
HEIGHTSCREEN = 700