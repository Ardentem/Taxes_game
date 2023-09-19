import json
import settlement
ret = settlement.settle()
print(ret)
print(type(ret[0]))