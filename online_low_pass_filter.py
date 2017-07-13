#!/usr/bin/env python2
"""
Created on Wed Jul 12 19:41:11 2017

Filter data using b, a from low pass filter

@author: gowtham
"""
from scipy.signal import butter
from ring_buffer import RingBuffer
import numpy as np

class OnlineButterLowPassFilter:
    def __init__(self, cutoff, frequency, order=6):
        nyq = 0.5 * frequency  # Nyqst frequency
        normal_cutoff = cutoff / nyq  # Normalized cutoff
        # Butterworth low pass filter
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        self.b = b
        self.a = a
        self.filtered_buffer = RingBuffer(self.a.size - 1)
        self.unfiltered_buffer = RingBuffer(self.b.size)

    def filterValue(self, input_data):
       self.unfiltered_buffer.add_element(input_data)
       yfilt = (np.sum(self.unfiltered_buffer.get_array()*self.b[::-1]) -
                np.sum(self.filtered_buffer.get_array()*self.a[:0:-1]))
       self.filtered_buffer.add_element(yfilt)
       return yfilt