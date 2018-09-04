# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 15:26:13 2018

@author: XY100075
"""

import xy as xy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data=xy.READ_DATA('sample')

bins,bins_count=xy.DATA_BIN(data.iloc[:,3:],10)
iv,good_bad,eff_rate=xy.DATA_IV(data.iloc[:,3:],bins)
xy.WRITE_BIN_IV('bin.txt',data.iloc[:,3:],bins,good_bad,iv)
#psi=xy.PSI_(data1)
combination=xy.DATA_COMBINE(data.iloc[:,3:],iv,0.1,0.6,0.6)
deny_rule,pass_overdue=xy.DENY_RULE(data.iloc[:,3:],coAmbination,[0.12,0.08,0.05])
xy.WRITE_REPORT('report_首逾2.xlsx',data.iloc[:,3:],eff_rate,iv,combination,deny_rule)
