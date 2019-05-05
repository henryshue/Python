#!/usr/bin/env python
#------coding=utf-8 -----------------

import json, copy
from httplib2 import Http
from lib.logsdeploytools import DeployLogger

global deployLogger
deployLogger = DeployLogger()
deployLogger.setConsoleLog(False)

def get_string_from_interface(curls):
    try:
        __,content = Http(timeout=60).request(curls, "GET", None)
        gdata = json.loads(content, 'utf-8')
        if gdata["code"] == 0:
            deployLogger.info(u"获取接口数据: URL=%s" %(curls))
            deployLogger.info(u"状态: [状态码: %s,信息: %s], 获取数据成功" % (gdata["code"], gdata["msg"]))
            return gdata
        else:
            deployLogger.info(u"获取接口数据: URL=%s" %(curls))
            deployLogger.info(u"状态: [状态码: %s,信息: %s], 获取数据失败，请检查应用编码或环境ID是否正确" % (gdata["code"], gdata["msg"]))
            return None
    except:
        deployLogger.error(u"接口不存在: URL = %s" %(curls))
        deployLogger.error(u"出现错误的可能性是：使用域名来访问的，请检查是否配置hosts或DNS域名解析")
        return None

def post_result_to_interface(curls):
    try:
        print(u"curls=%s"%(curls))
        __,content = Http(timeout=30).request(curls,"POST", None)
        print(u"content=%s"%(content))
        gdata = json.loads(content, 'utf-8')
        print(u"gdata=%s"%(gdata["code"]))
        if gdata["code"] ==0:
            deployLogger.info(u"更新接口数据: URL=%s" %(curls))
            deployLogger.info(u"状态:[状态码: %s,信息: %s], 更新【POST】数据成功" %(gdata["code"], gdata["msg"]))
            return True
        else:
            deployLogger.info(u"更新接口数据: URL=%s" % (curls))
            deployLogger.info(u"状态: [状态码: %s,信息: %s], 更新数据失败，请检查接口是否正确" % (gdata["code"], gdata["msg"]))
            return None
    except:
        deployLogger.error(u"接口不存在: URL = %s" %(curls))
        return None

def post_form_data_to_interface(curls, data):
    headers={}
    headers = dict(headers.items() + {'Content-type': 'application/json', 'accept-encoding':'identity'}.items())
    try:
        __,content = Http(timeout=10).request(curls, "POST", json.dumps(data, ensure_ascii=True), headers)
        pdata = json.loads(content, 'utf-8')
        if pdata["code"] ==0:
            deployLogger.info(u"更新接口数据: URL=%s" %(curls))
            deployLogger.info(u"状态:[状态码: %s,信息: %s], 更新【POST】成功" %(pdata["code"], pdata["msg"]))
            return True
        else:
            deployLogger.info(u"更新接口数据: URL=%s" % (curls))
            deployLogger.info(u"状态: [状态码: %s,信息: %s], 更新数据失败，请检查接口是否正确" % (pdata["code"], pdata["msg"]))
            return None
    except:
        deployLogger.error(u"接口不存在: URL = %s" %(curls))
        return None

def get_unpack_data(ifurl):
    flowstr = get_string_from_interface(ifurl)
    if flowstr != None:
        ti = flowstr["data"]["taskId"]
        gl = flowstr["data"]["globalParams"]
        fl = flowstr["data"]["flows"]
        pa = flowstr["data"]["params"]
        pg = flowstr["data"]["packageAddress"]
        return (ti, gl, fl, pa, pg)
    else:
        return (None, None, None, None, None)

def get_unpack_ssu_data(ifurl):
    flowstr = get_string_from_interface(ifurl)
    if flowstr != None:
        passu = flowstr["data"]
        return passu
    else:
        return None

def get_db_user_password(ifurl):
    gdbup = get_string_from_interface(ifurl)
    if gdbup != None:
        gdbup = gdbup["data"]
        return gdbup
    else:
        return None

def getNacessaryData(namespace, appCode, params):
    try:
        resuleDic={}
        for u in params['apps'][appCode].keys():
            if u == 'params':
                resultDict = copy.deepcopy(dict(params['apps'][appCode]['params'].items() + resultDict.items()))
            else:
                resultDict[u] = copy.deepcopy(params['app'][appCode][u])
        if 'depends' in params['namespaces'][namespace].keys():
            for i in params['namespace'][namespace]['depends']:
                for h in i.keys():
                    resultDict[h]               = copy.deepcopy(params['apps'][i[h]['appCode']])
                    resultDict[h]['envParams']  = copy.deepcopy(i[h]['envParams'])
        return resultDict
    except:
        return None

