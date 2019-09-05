#coding: utf-8
import sys, os, yaml, re, json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONF_YAML = os.path.join(BASE_DIR, 'var-conf.yaml')
RESULT_DIR = os.path.join(BASE_DIR, 'result')


class VarConvertion(object):
    def __init__(self):
        self.confDict = self.getVarConf()

    def run(self):
        if not self.confDict: return False
        for filePath in self.getTargetFilePath():
            self.convertData(filePath)
    
    def getVarConf(self):
        if not os.path.exists(CONF_YAML): return {}
        with open(CONF_YAML, 'rt', encoding='utf-8') as f:
            confDict = yaml.load(f.read(), Loader=yaml.SafeLoader)
        return confDict
    
    def getTargetFilePath(self):
        filePathSet = set()
        for root, _, files in os.walk(BASE_DIR):
            if 'result' in root: continue
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    filePath = os.path.join(root, file)
                    if os.path.getsize(filePath) > 0:
                        filePathSet.add(filePath)
        return filePathSet
    
    def convertData(self, filePath):
        targetFilePath = self.checkTargetDir(filePath)
        with open(filePath, 'rb') as f:
            contentList = f.readlines()

        noteFlag, funcFlag, lastLine = False, True, b''
        with open(targetFilePath, 'wb') as f:
            self.clsFlag = False
            for line in contentList:
                lineTemp = re.sub(rb'\s+', b'', line)
                if lineTemp.startswith(b'"""') and not lineTemp.lstrip(
                    b'"""').endswith(b'"""'):
                    noteFlag = not noteFlag
                    if noteFlag: funcFlag = False
                    
                if noteFlag: 
                    if not funcFlag:
                        funcName = self.getFuncName(lastLine)
                        funcFlag = True
                    line = self.replaceVarData(filePath, funcName, line)
                f.write(line)
                lastLine = line
    
    def checkTargetDir(self, filePath):
        targetFilePath = filePath.replace(BASE_DIR, RESULT_DIR)
        targetDir = os.path.dirname(targetFilePath)
        if not os.path.exists(targetDir): os.makedirs(targetDir)
        return targetFilePath
    
    def getFuncName(self, content):
        if not b"class" in content and not b'def' in content: return False
        self.clsFlag = True if b'class' in content else False

        funcName = re.sub(rb'class|def', b'', content)
        try:
            funcName = re.compile(rb'(\S+.*?)\(').findall(funcName)[0]
        except:
            funcName = re.compile(rb'(\S+.*?):').findall(funcName)[0]
        funcName = str(funcName, encoding='utf-8')
        if self.clsFlag: self.clsName = funcName
        return funcName
 
    def replaceVarData(self, filePath, funcName, content):
        if not funcName: return content
        if self.confDict.get(filePath, None):
            if self.confDict[filePath].get(self.clsName, None):
                tempDict = {}
                if self.clsFlag:
                    tempDict = self.confDict[filePath][self.clsName]
                else:
                    if self.confDict[filePath][self.clsName].get(funcName, None):
                        tempDict = self.confDict[filePath][self.clsName][funcName]
                try:
                    prefix = re.compile(rb'(\s+)\S+').findall(content)[0]
                    prefix = str(prefix, encoding='utf-8') + '\t'
                except:
                    prefix = '\t'
                for key in tempDict:
                    value = tempDict[key]
                    if isinstance(value, dict):
                        value = self.formatDictData(value, prefix)
                    elif isinstance(value, list):
                        value = self.formatListData(value, prefix)
                    else:
                        value = str(value)
                    content = content.replace(bytes(key, 'utf-8'), bytes(value, 'utf-8'))
        return content
    
    def formatDictData(self, data, prefix):
        value = json.dumps(data, indent=4)
        value = value.replace('\n', '\n'+prefix)
        return value
    
    def formatListData(self, data, prefix):
        tPrefix = '\r\n' + prefix
        return "["+tPrefix + tPrefix.join(data) + "]"
    
    def writeConfYaml(self, clsName, varData, *, clsData={}):
        try:
            raise Exception
        except:
            exc_info = sys.exc_info()[2].tb_frame.f_back.f_code
        fileName, funcName = exc_info.co_filename, exc_info.co_name
        
        if not self.confDict: self.confDict = {}
        if not fileName in self.confDict: self.confDict[fileName] = {}
        self.confDict[fileName][clsName] = clsData
        self.confDict[fileName][clsName][funcName] = varData
        with open(CONF_YAML, 'wt', encoding='utf-8') as f:
            yaml.dump(self.confDict, f)


if __name__ == "__main__":
    VarConvertion().run()
    # VarConvertion().writeConfYaml(self.__class__.__name__, funcData, clsData=clsData)
