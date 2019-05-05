#!/usr/bin/env python
#------coding: utf-8-----------------
import sys
from lib.logsdeploytools import DeployLogger
reload(sys)
sys.setdefaultencoding('utf-8')

deployLogger = DeployLogger()
deployLogger.setConsoleLog(True)

def ansible_errorMessage_to_Chinese(darkResult, title, deployIp, deployuser, tfileName=''):
    for (failHostname, failResult) in darkResult['dark'].items():
        if failResult['failed']:
            if failResult['msg'] == 'Authentication failure.':
                deployLogger.error(u"|---->%s==> Host:%s not exists%suser or %s password error"%(title, failHostname, deployuser, deployuser))
                deployLogger.error(u"|---->%s==> Error info:%s"%(title, failResult['msg']))
                sys.exit(1)
            elif 'AnsibleUndefineVariable' in failResult['msg']:
                deployLogger.error(u"|---->%s==> Error because deploy%s on process used template engin, just have variable, but not have value of variable, the following info is raised by asnbile"%(title, tfileName))
                deployLogger.error(u"|---->%s==> Error info:%s"%(title, failResult['msg']))
            elif 'SSH encountered an unknown error during the connection' in failResult['msg']:
                deployLogger.error(u"|---->%s==> Host:%s use%s SSH connected to Host:%s encountered error in the process, maybe the network is blocked, pls check if"%(title, deployIp, deployuser, failHostname))
                deployLogger.error(u"|---->%s==> Error info:%s" % (title, failResult['msg']))
                sys.exit(1)
            else:
                deployLogger.error(u"|---->%s==> Errors in the Ansible, is in deploy processing, pls connect by auto deploy developer"%(title, fialHostname))
                deployLogger.error(u"|---->%s==> Error info:%s" % (title, failResult['msg']))
                sys.exit(1)

