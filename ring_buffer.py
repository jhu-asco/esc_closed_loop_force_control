#!/usr/bin/env python
"""
Ring buffer
"""
import numpy as np


class RingBuffer:
    """
    A simple FIFO buffer with specified buffer size
    """

    def __init__(self, buffer_size=1):
        """
        Constructor.
        Instantiates the buffer
        """
        self.array = np.zeros(buffer_size)
        self.idx = -1
        self.buffer_size = buffer_size

    def add_element(self, value):
        """
        Adds an element to the buffer and
        updates the internal index
        Parameters:
        value -- Value to be added to buffer
        """
        self.idx = (self.idx + 1) % self.buffer_size
        self.array[self.idx] = value

    def get_array(self):
        """
        Get back the fifo array sorted according to
        the arrival time
        """
        idx_old = (self.idx + 1) % self.buffer_size
        return np.hstack((self.array[idx_old:], self.array[:idx_old]))

if __name__ == "__main__":
    # Test ring buffer
    ring_buffer = RingBuffer(3)
    for i in range(5):
        ring_buffer.add_element(i)
    print ring_buffer.get_array()
    print ring_buffer.array
