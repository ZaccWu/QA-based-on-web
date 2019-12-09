# for the function testing
import sys
import pandas as pd
from pandas import Series, DataFrame
from KGDataprocessing import Question

que=Question()
# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
enablePrint()
result=que.question_process("李连杰演过哪些电影")
print(result)
