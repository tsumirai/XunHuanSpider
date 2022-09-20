import os


class SaveTxt:
	def saveTxt(self, contentData, filePath):
		if not os.path.exists(filePath):
			os.makedirs(filePath, mode=0o755, exist_ok=True)
		fileName = contentData['title']
		fw = open(filePath + '/' + fileName + '.txt', 'w', encoding='utf-8')
		for k, v in contentData.items():
			# print(k)
			# print(v)
			if isinstance(v, list):
				imgUrl = "\n".join(v)
				fw.write(k + ' : ' + imgUrl)
			else:
				fw.write(k + ' : ' + v)
			fw.write('\n')
			fw.write('\n')
		fw.close()
