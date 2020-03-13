# Copyright 2020 Klaifer Garcia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import copy
import numpy as np


class Puzzle:
    RIGTH = 1
    LEFT = -1
    UP = -3
    DOWN = 3

    def solve(self, init, target):
        initial, target = Puzzle._prepare(init, target)
        queue = [{'parent': None, 'board': initial}]
        hqueue = np.zeros(987654322, dtype=bool)

        iqueue = 0
        while len(queue) > iqueue:
            newstates = self._gettransition(queue[iqueue], iqueue)
            for state in newstates:
                if Puzzle._equals(state['board'], target):
                    self._printsolution(state, queue)
                    return

            newstates = list(filter(lambda x: not hqueue[Puzzle._hash(x)], newstates))
            for state in newstates:
                hqueue[Puzzle._hash(state)] = True

            queue += newstates
            iqueue += 1

        print('Not found')

    def _printsolution(self, node, queue):
        if node['parent'] is None:
            move = 0
        else:
            move = self._printsolution(queue[node['parent']], queue)

        values = [str(x) if x is not None else ' ' for x in node['board']['values']]
        print("""--------------------------------
        move: {0}, board: {1} {2} {3}
                         {4} {5} {6}
                         {7} {8} {9}
        """.format(*(['{:02d}'.format(move)] + values)))

        return move + 1

    @staticmethod
    def _hash(node):
        values = node['board']['values']

        code = 0
        for v in values:
            code = code * 10 + (v if v is not None else 9)

        return code

    @staticmethod
    def _equals(p1, p2):
        if p1['blank'] != p2['blank']:
            return False
        for i in range(0, 8):
            if p1['values'][i] != p2['values'][i]:
                return False
        return True

    def _gettransition(self, node, inode):
        newpos = []
        blank = node['board']['blank']
        if blank in [0, 1, 3, 4, 6, 7]:
            newpos.append(Puzzle._move(node, self.RIGTH, inode))
        if blank in [1, 2, 4, 5, 7, 8]:
            newpos.append(Puzzle._move(node, self.LEFT, inode))
        if blank in [0, 1, 2, 3, 4, 5]:
            newpos.append(Puzzle._move(node, self.DOWN, inode))
        if blank in [3, 4, 5, 6, 7, 8]:
            newpos.append(Puzzle._move(node, self.UP, inode))

        return newpos

    @staticmethod
    def _move(node, step, parent):
        board = copy.deepcopy(node['board'])
        Puzzle._change(board['values'], board['blank'], board['blank'] + step)
        board['blank'] += step
        return {'parent': parent, 'board': board}

    @staticmethod
    def _change(array, p1, p2):
        v = array[p2]
        array[p2] = array[p1]
        array[p1] = v

    @staticmethod
    def _prepare(init, tgt):
        init = [item for sublist in init for item in sublist]
        tgt = [item for sublist in tgt for item in sublist]

        nodeinit = {'blank': init.index(None), 'values': init}
        nodetarget = {'blank': tgt.index(None), 'values': tgt}

        return nodeinit, nodetarget


if __name__ == "__main__":
    initial = [[8, 7, 6], [None, 4, 1], [2, 5, 3]]
    target = [[1, 2, 3], [4, 5, 6], [7, 8, None]]

    puzzle = Puzzle()
    puzzle.solve(initial, target)
