import os
import logging
from datetime import date, datetime


class Logger(object):
    '''
    def __init__(self):
        name = date.today().strftime('%m-%d-%y')
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        directory = ROOT_DIR + '/logs/onboarding/'
        self.file = directory + name + '.txt'
    '''
    logType = "onboarding"

    def __init__(self, logType='logs'):
        name = date.today().strftime('%m-%d-%y')
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        directory = ROOT_DIR + '/logs/'
        self.file = directory + name + '.txt'

    def refresh(self):
        name = date.today().strftime('%m-%d-%y')
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        directory = ROOT_DIR + '/logs/'
        self.file = directory + name + '.txt'

    def request(self, content):
        self.refresh()
        f = open(self.file, 'a+')
        f.write('-----------------------------------------------------\n')
        f.write('Request: \n')
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' : ' + content + '\n')
        f.close()

    def response(self, content):
        self.refresh()
        f = open(self.file, 'a+')
        f.write('Response: \n')
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' : ' + content + '\n')
        f.write('*****************************************************\n')
        f.close()

    def info(self, tag, content):
        self.refresh()
        f = open(self.file, 'a+')
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + tag + ': ' + content + '\n')
        f.close()

    def newline(self):
        self.refresh()
        f = open(self.file, 'a+')
        f.write('\n*****************************************************\n')
        f.close()

    def error(self, content):
        self.refresh()
        f = open(self.file, 'a+')
        f.write('Error: \n')
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' : ' + content + '\n')
        f.close()
