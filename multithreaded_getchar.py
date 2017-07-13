#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 16:15:26 2017

@author: gowtham
"""
import sys
import threading
import time


class MultiThreadedGetChar:

    def __init__(self):
        self.__output__ = ''
        self.t = threading.Thread(name='Child', target=self.readInput)
        self.__lock__ = threading.Lock()
        self.__exit_condition__ = False

    def __enter__(self):
        self.t.start()
        return self

    def readInput(self):
        exit_condition = False
        while not exit_condition:
            print "Enter character"
            val = sys.stdin.read(1)
            if ord(val) == 10:
                continue
            print "Val: ", val
            self.__lock__.acquire()
            self.__output__ = val
            exit_condition = self.__exit_condition__
            self.__lock__.release()

    def __call__(self):
        self.__lock__.acquire()
        val = self.__output__
        self.__lock__.release()
        return val

    def __exit__(self, *args):
        print "Exiting Thread! Press any key to continue"
        self.__lock__.acquire()
        self.__exit_condition__ = True
        self.__lock__.release()
        self.t.join()

# Test code
if __name__ == "__main__":
    with MultiThreadedGetChar() as readIn:
        out = ''
        while out == '':
            readIn.getInput()
            out = readIn()
            time.sleep(1)
        print out
