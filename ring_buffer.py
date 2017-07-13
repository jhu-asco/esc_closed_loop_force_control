#!/usr/bin/env python
"""
Ring buffer
"""
import numpy as np


class RingBuffer:
    def __init__(self, buffer_size=1):
        self.array = np.zeros(buffer_size)
        self.idx = -1
        self.buffer_size = buffer_size

    def add_element(self, value):
        self.idx = (self.idx + 1) % self.buffer_size
        self.array[self.idx] = value

    def get_array(self):
        idx_old = (self.idx + 1) % self.buffer_size
        return np.hstack((self.array[idx_old:], self.array[:idx_old]))

if __name__ == "__main__":
    # Test ring buffer
    ring_buffer = RingBuffer(3)
    for i in range(5):
        ring_buffer.add_element(i)
    print ring_buffer.get_array()
    print ring_buffer.array