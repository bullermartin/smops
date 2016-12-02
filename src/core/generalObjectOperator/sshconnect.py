# -*- coding:utf-8 -*-
#!/usr/bin/env python

"""
@version: ??
@author: Ron
@software: PyCharm
@file: sshconnect.py
@time: 2016/6/23 16:05
"""


import paramiko

class sshConnect(object):

    def __init__(self,host, port, username, password):
        port = int(port)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, port, username, password)

    def excute(self,command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            self.stdout = stdout.readlines()
            self.stderr = stderr.readlines()
            return True
        except:
            return False

    def getStdout(self):
        return self.stdout

    # def stdin(self,args):
    #     return True
    #

    def getStderr(self):
        return self.stderr

    def close(self):
        try:
            self.ssh.close();
            return True
        except:
            return False
