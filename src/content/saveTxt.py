import os
from src.logger import logger


class SaveTxt:
    def saveTxt(self, contentData, filePath):
        try:
            if not os.path.exists(filePath):
                os.makedirs(filePath, mode=0o755, exist_ok=True)
            fileName = contentData['title']
            fw = open(filePath + '/' + fileName +
                      '.txt', 'w', encoding='utf-8')
            for k, v in contentData.items():
                if isinstance(v, list):
                    imgUrl = "\n".join(v)
                    fw.write(k + ' : ' + imgUrl)
                else:
                    fw.write(k + ' : ' + v)
                fw.write('\n')
                fw.write('\n')
        except Exception as result:
            logger.error(
                result.__traceback__.tb_frame.f_globals['__file__']+':'+str(result.__traceback__.tb_lineno)+'|'+repr(result))
        finally:
            fw.close()
