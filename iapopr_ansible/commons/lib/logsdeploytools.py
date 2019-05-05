#!/usr/bin/env python
#------coding: utf-8-----------------

import logging
import os
import uuid
from lib.configdeploytools import deployconfig

class Logger:
    def __init__(self, path="./", logName="autodeploy.log"):
        if path.endswith('/'):
            path = path.rstrip('/')
        if not os.path.exists(path):
            os.mkdir(path)

        if (logName.endswith(".log")):
            self.path = path + '/' + logName.replace("./log", "_runningLOg.log")
            self.consolePath = path + '/' + logName.replace(".log", "_consleLog.log")
        else:
            self.path = path + '/' + logName + '_runningLog'
            self.consolePath = path + '/' + logName + '_consoleLog'

        self.rootLogger = logging.getLogger("")
        consoleLogID = str(uuid.uuid1())
        fileLogID = str(uuid.uuid1())

        self.consoleLogger = logging.getLogger(consoleLogID)
        self.fileLogger = logging.getLogger(fileLogID)
        self.logFmt = '%(asctime)s [%(levelname)s] %(message)s'
        self.consoleFmt = '%(levelno)s %(asctime)s %(message)s'
        self.rootLogger.setLevel(logging.DEBUG)

        #run logging file handler
        self.fileHandler = logging.FileHandler(self.path)
        self.fileHandler.setFormatter(logging.Formatter(self.logFmt))
        self.fileLogger.addHandler(self.fileHandler)

        #run logging handler
        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setFormatter(logging.Formatter(self.consoleFmt))
        self.consoleLogger.addHandler(self.consoleHandler)

        #run logging file handler
        self.consoleFileHandler = logging.FileHandler(self.consolePath)
        self.consoleFileHandler.setFormatter(logging.Formatter(self.logFmt))
        self.consoleLogger.addHandler(self.consoleFileHandler)

    def setLogFile(self, path, logFileName):
        if not os.path.exists(path):
            os.makedirs(path)

        if (logFileName.endswith(".log")):
            self.path = path + '/' + logFileName.replace(".log", "_runningLog.log")
            self.consolePath = path + '/' + logFileName.replace(".log", "_consoleLog.log")
        else:
            self.path = path + '/' + logFileName + '_runningLog'
            self.consolePath = path + '/' + logFileName + '_consoleLog'

        lastHandler = self.fileHandler
        self.fileHandler = logging.FileHandler(self.path)
        self.fileHandler.setFormatter(logging.Formatter(self.logFmt))
        self.fileLogger.addHandler(self.fileHandler)
        self.fileLogger.removeHandler(lastHandler)

        lastConsoleHandler = self.consoleHandler
        self.consileFileHandler = logging.FileHandler(self.consolePath)
        self.consileFileHandler.setFormatter(logging.Formatter(self.logFmt))
        self.consoleLogger.addHandler(self.consoleFileHandler)
        self.consoleLogger.removeHanlder(lastConsoleHandler)

        self.infoWithNumberSign('deploy log location: ' + self.consolePath)
        self.infoWithNumberSign('trace log location: ' + self.path)

    def setConsoleLog(self, bools):
        if bools == False:
            self.consoleLogger.setLevel(logging.WARNING)
        else:
            self.consoleLogger.setLevel(logging.INFO)

    #NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
    def debug(self, message):
        self.fileLogger.debug(message)

    def safeDebug(self, message):
        self.fileLogger.error(message)

    def info(self, message):
        messageWithColor = '\x1b[1;32m' + message + '\x1b[0m'
        self.fileLogger.info(messageWithColor)
        self.consoleLogger.info(message)

    def warning(self, message):
        messageWithColor = '\x1b[1;33m' + message + '\x1b[0m'
        self.fileLogger.warning(messageWithColor)
        self.consoleLogger.warning(message)

    def error(self, message):
        messageWithColor = '\x1b[1;31m' + message + '\x1b[0m'
        self.fileLogger.error(messageWithColor)
        self.consoleLogger.error(message)

    def critical(self, message):
        messageWithColor = '\x1b[1;7;31m' + message + '\x1b[0m'
        self.fileLogger.critical(message)
        self.consoleLogger.critical(messageWithColor)

    def infoTitle(self, message):
        messageWithColor = '\x1b[1;34m' + message + '\x1b[0m'
        self.fileLogger.info(message)
        self.consoleLogger.info(messageWithColor)

    def infoSubHeading(self, message):
        lenOfHyphen = int((50 - len(message))/2)
        messageWithHyphen = '-' * lenOfHyphen + message + '-' * lenOfHyphen
        self.info(messageWithHyphen)

    #info logger begin with #
    def infoWithNumberSign(self, message):
        pre = '\x1b[1;32m # '
        messageWithColor = pre + message + '\x1b[0m'
        self.fileLogger.info(message)
        self.consoleLogger.info(messageWithColor)

    #warning logger begin with #
    def warningWithNumberSign(self, message):
        pre = '\x1b[1;33m # '
        messageWithColor = pre + message + '\x1b[0m'
        self.fileLogger.warning(message)
        self.consoleLogger.warning(messageWithColor)

    def infoJboss(self, message):
        lastLogFmt = self.logFmt
        lastConsoleFmt = self.consoleFmt
        noFormat = '%(message)s'

        self.fileHandler.setFormatter(logging.Formatter(noFormat))
        self.consoleFileHandler.setFormatter(logging.Formatter(noFormat))
        self.consoleHandler.setFormatter(logging.Formatter(noFormat))

        self.fileLogger.info(message)
        self.consoleLogger.info(message)

        self.fileHandler.setFormatter(logging.Formatter(lastLogFmt))
        self.consoleFileHandler.setFormatter(logging.Formatter(lastLogFmt))
        self.consoleHandler.setFormatter(logging.Formatter(lastConsoleFmt))


class DeployLogger(Logger):
    def __init__(self, appid=''):
        deploydir = deployconfig().get_logs_dir()
        if not appid:
            self.path = deploydir
            self.logName = "autodeploy.log"
        else:
            self.path = deploydir + "/%s/"%(appid)
            self.logName = "autodeploy.log"
        Logger.__init__(self, self.path, self.logName)















