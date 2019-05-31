import requests
import base64
import os
import time
import json

user = 123456
passwd = b'base64encoded password'

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


def auto_connect():
	t = time.strftime("%Y-%m-%d %H:%M:%S")
	log = t + " %s"
	status = check_connect()
	if status:
		print("connected")
		log = log % "connected"
		r = True
	else:
		r, msg = connect()
		if r:
			print("success")
			log = log % "success"
		else:
			print("failed, %s" % msg)
			log = log % ("failed" + msg)
			r = False
	os.system("echo %s >> connect.log" % log)
	return r

def main():
	r = False
	try:
		r = auto_connect()
	except:
		pass

if __name__ == '__main__':
	main()
	# time.strftime("%Y-%m-%d %H:%M:%S")
