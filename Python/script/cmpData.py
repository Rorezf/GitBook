#coding: utf-8
import copy

def cmpData(srcData, dstData):
    if isinstance(srcData, dict): return checkDict(srcData, dstData)
    elif isinstance(srcData, set): return checkSet(srcData, dstData)
    elif isinstance(srcData, list): return checkList(srcData, dstData)
    elif isinstance(srcData, tuple): return checkTuple(srcData, dstData)
    elif isinstance(srcData, str): return checkStr(srcData, dstData)
    elif isinstance(srcData, bool): return checkBool(srcData, dstData)
    else: return checkOthers(srcData, dstData)

def checkDict(srcData, dstData):
    if not isinstance(dstData, dict): return False
    sKeySet, dKeySet = set(srcData.keys()), set(dstData.keys())
    if sKeySet-dKeySet or dKeySet-sKeySet: return False
    else:
        for key in srcData: 
            if not cmpData(srcData[key], dstData[key]): return False
    return True

def checkSet(srcData, dstData):
    if not isinstance(dstData, set): return False
    if srcData-dstData or dstData-srcData: return False
    return True

def checkTuple(srcData, dstData):
    if not isinstance(dstData, tuple): return False
    if len(srcData) != len(dstData): return False
    else:
        srcDataCp = sorted(copy.deepcopy(srcData))
        dstDataCp = sorted(copy.deepcopy(srcData))
        for i in range(len(srcDataCp)): 
            if not cmpData(srcDataCp[i], dstDataCp[i]): return False
    return True

def checkStr(srcData, dstData):
    if not isinstance(dstData, str): return False
    if srcData != dstData: return False
    return True

def checkBool(srcData, dstData):
    if not isinstance(dstData, bool): return False
    if srcData != dstData: return False
    return True

def checkOthers(srcData, dstData):
    if srcData != dstData: return False
    return True

def checkList(srcData, dstData):
    if not isinstance(dstData, list): return False
    if len(srcData) != len(dstData):
        return False
    else:
        srcDictList, dstDictList = [], []
        for i in range(len(srcData)):
            if isinstance(srcData[i], dict): srcDictList.append(srcData[i])
            if isinstance(dstData[i], dict): dstDictList.append(dstData[i])
        if len(srcDictList) != len(dstDictList): return False
        
        srcDataCp = copy.deepcopy(srcData)
        dstDataCp = copy.deepcopy(dstData)
        for i in range(len(srcDictList)): 
            srcDataCp.remove(srcDictList[i])
            dstDataCp.remove(dstDictList[i])
        srcDataCp.sort()
        dstDataCp.sort()

        for i in range(len(srcDataCp)): 
            if not cmpData(srcDataCp[i], dstDataCp[i]): return False
        if not checkDictOfList(srcDictList, dstDictList): return False
    return True

def checkDictOfList(srcDictList, dstDictList):
    mappingList, ignoerList = [], []
    for i in range(len(srcDictList)):
        for j in range(len(dstDictList)):
            if dictMapping(srcDictList[i], dstDictList[j]):
                mappingList.append([srcDictList[i], dstDictList[j]])    
    
    if len(mappingList) != 1:
        passCounter = 0
        for item in mappingList: 
            if cmpData(item[0], item[1]): passCounter += 1
            else: ignoerList.append(item)
        if passCounter != len(srcDictList): return False
        for item in ignoerList: mappingList.remove(item)

    elif len(mappingList) != len(srcDictList): return False
    for item in mappingList: 
        if not cmpData(item[0], item[1]): return False
    return True

def dictMapping(sDict, dDict):
    sKeySet, dKeySet = set(sDict.keys()), set(dDict.keys())
    if sKeySet - dKeySet or dKeySet - sKeySet: return False
    for key in sDict:
        if isinstance(sDict[key], dict):
            if not isinstance(sDict[key], dict): return False
            return dictMapping(sDict[key], dDict[key])
    return True


dictA = {'accessTypes': ['3GPP_ACCESS'],
 'adminState': 'Committed',
 'default': True,
 'nfSets': [{'nfId': ['efc275b8-ecd3-400d-smf1-9a000bf5f001',
                      'efc275b8-ecd3-400d-smf1-9a000bf5f002',
                      'efc275b8-ecd3-400d-smf1-9a000bf5f003'],
             'nfType': 'SMF',
             'nrfUri': 'http://172.0.4.170:8008/nnrf-nfm/v1/nf-instances/efc275b8-ecd3-400d-nrf1-9a000bf5f005',
             'setId': 'setId2'},
            {'nfId': ['efc275b8-ecd3-400d-amf1-9a000bf5f001',
                      'efc275b8-ecd3-400d-amf1-9a000bf5f002',
                      'efc275b8-ecd3-400d-amf1-9a000bf5f003',
                      'efc275b8-ecd3-400d-amf1-9a000bf5f004'],
             'nfType': 'AMF',
             'nrfUri': 'http://172.0.4.170:8008/nnrf-nfm/v1/nf-instances/efc275b8-ecd3-400d-nrf1-9a000bf5f004',
             'setId': 'setId1'},
            {'nfId': ['http://172.0.4.170:8008/nnrf-nfm/v1/nf-instances/efc275b8-ecd3-400d-nrf1-9a000bf5f001',
                      'http://172.0.4.170:8008/nnrf-nfm/v1/nf-instances/efc275b8-ecd3-400d-nrf1-9a000bf5f002',
                      'http://172.0.4.170:8008/nnrf-nfm/v1/nf-instances/efc275b8-ecd3-400d-nrf1-9a000bf5f003'],
             'nfType': 'NRF',
             'nrfUri': 'http://172.0.4.170:8008/nnrf-nfm/v1/nf-instances/efc275b8-ecd3-400d-nrf1-9a000bf5f006',
             'setId': 'setId3'}],
 'ratType': ['NR', 'EUTRA', 'WLAN', 'VIRTUAL'],
 'sNssai': [{'sst': 1},
            {'sd': 'A02B01', 'sst': 2},
            {'sst': 3},
            {'sd': 'A04B01', 'sst': 4}],
 'supportedFeatures': '910abcd',
 'timeStamp': '2019/7/17'}

dictB = {'accessTypes': ['3GPP_ACCESS'],
 'adminState': 'Committed',
 'default': True,
 'nfSets': [{'nfId': ['efc275b8-ecd3-400d-smf1-9a000bf5f001',
                      'efc275b8-ecd3-400d-smf1-9a000bf5f002',
                      'efc275b8-ecd3-400d-smf1-9a000bf5f003'],
             'nfType': 'SMF',
             'nrfUri': 'http://172.0.4.170:8008/nnrf-nfm/v1/nf-instances/efc275b8-ecd3-400d-nrf1-9a000bf5f005',
             'setId': 'setId2'},
            {'nfId': ['efc275b8-ecd3-400d-amf1-9a000bf5f001',
                      'efc275b8-ecd3-400d-amf1-9a000bf5f002',
                      'efc275b8-ecd3-400d-amf1-9a000bf5f003',
                      'efc275b8-ecd3-400d-amf1-9a000bf5f004'],
             'nfType': 'AMF',
             'nrfUri': 'http://172.0.4.170:8008/nnrf-nfm/v1/nf-instances/efc275b8-ecd3-400d-nrf1-9a000bf5f004',
             'setId': 'setId1'},
            {'nfId': ['http://172.0.4.170:8008/nnrf-nfm/v1/nf-instances/efc275b8-ecd3-400d-nrf1-9a000bf5f001',
                      'http://172.0.4.170:8008/nnrf-nfm/v1/nf-instances/efc275b8-ecd3-400d-nrf1-9a000bf5f002',
                      'http://172.0.4.170:8008/nnrf-nfm/v1/nf-instances/efc275b8-ecd3-400d-nrf1-9a000bf5f003'],
             'nfType': 'NRF',
             'nrfUri': 'http://172.0.4.170:8008/nnrf-nfm/v1/nf-instances/efc275b8-ecd3-400d-nrf1-9a000bf5f006',
             'setId': 'setId3'}],
 'ratType': ['NR', 'EUTRA', 'WLAN', 'VIRTUAL'],
 'sNssai': [{'sst': 3},
            {'sd': 'A02B01', 'sst': 2},
            {'sst': 1},
            {'sd': 'A04B01', 'sst': 4}],
 'supportedFeatures': '910abcd',
 'timeStamp': '2019/7/17'}


if __name__ == "__main__":
    status = cmpData(dictA, dictB)
    print(status)