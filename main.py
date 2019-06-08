import requests
import base64
import os
import time
import json

user = 123456
passwd = b'base64encoded password'
ssid = "Shu(ForAll)"

def isShuForAll():
	lines = []
	with os.popen("iwconfig 2>&1 | grep '%s'" % ssid, "r") as out:
		lines = out.readlines()
	if len(lines) == 0:
		return False
	else:
		return True


def check_connect():
	r = requests.get("http://10.10.9.9:8080")
	if "success.jsp" in r.url:
		return True
	else:
		return False


def connect():
	r = requests.get("http://123.123.123.123/")
	query_string = r.text
	st = query_string.find("index.jsp?") + 10
	end = query_string.find("'</script>")
	query_string = query_string[st:end]

	t = base64.b64decode(passwd).decode()

	data = {"userId": user, "password": t, "passwordEncrypt": "false", "queryString": query_string, "service": "", "operatorPwd": "", "operatorUserId": "", "validcode": ""}
	r = requests.post("http://10.10.9.9:8080/eportal/InterFace.do?method=login", data=data)
	r.encoding = "utf-8"
	resp = r.json()
	if resp["result"] == "success":
		return True, ""
	else:
		return False, resp["message"]


def start_connect():
	t = time.strftime("%Y-%m-%d %H:%M:%S")
	if not isShuForAll():
		print("%s not connnect shuforall" % t)
		return
	status = check_connect()
	if status:
		print("%s already connected" % t)
	else:
		r, msg = connect()
		if r:
			print("%s connect success" % t)
		else:
			print("%s connect failed: %s" % (t, msg))


def main():
	try:
		start_connect()
	except Exception as e:
		print(e)

if __name__ == '__main__':
	main()
