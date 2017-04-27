from js9 import j
import multiprocessing
import unittest
import sys


class DebuggerTest(unittest.TestCase):

    def test_embed_debug_enable(self):
        p = j.sal.process.executeAsync(
            'jspython', args=["embed_debugger.py", 'True'])
        line = p.stdout.readline()
        self.assertEqual(line.decode().strip(), 'DEBUG STARTED')
        p.kill()
        p.wait()

    def test_embed_debug_disable(self):
        p = j.sal.process.executeAsync(
            'jspython', args=['embed_debugger.py', 'False'])
        p.wait(timeout=2)


if __name__ == '__main__':
    unittest.main()
