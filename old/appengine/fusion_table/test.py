# coding=utf-8
import json

if __name__ == "__main__":
	test_str = u"ניסיון"
	jso = [{1: test_str, 2: test_str}, {1: test_str, 2: test_str}]
	json.dump(jso, open("./test.json", "w+"))