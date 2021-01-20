# -*- coding: utf-8 -*-
import moduleAI as py_test

damier = py_test.Damier("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

pos_ini = py_test.VectorInt([-42])
pos_fin = py_test.VectorInt([-42])
prom = py_test.VectorInt([-42])

py_test.alpha_beta_exploration(test_damier, pos_ini, pos_fin, prom, 5)

assert py_test.__version__ == "0.0.1"
assert len(pos_ini) == 1
assert len(pos_fin) == 1
assert len(prom) == 1
assert pos_ini[0] = 52
assert pos_fin[0] = 36
assert prom[0] == -1

