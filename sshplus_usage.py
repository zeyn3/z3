import os
import sshplus
import logplus
try:
	import dev_settings
except Exception as e:
	print(e)


logger = logplus.LogPlus(dev_settings.LOG_FILE_PATH)
logger.log_plus("pli", "Logging started - all good ...")

"""
SCENARIO 1: TESTED: OK
	- Authenticate as the current user with a password
	- run single command on a single host
"""
# # The default values if not specified explicitly:  
# # SSH_USER=None # uses the current user
# # SSH_PASSWD=None # prompts for the current user's password
# # SSH_PK_PATH=None # no rivate key auth is used
# # SSH_PK_PASS=None # no rivate key auth is used
# # SSH_HOSTKEY_AUTO_ADD=False # RejectPolicy is active
# # SSH_HOSTKEY_PATH=None # uses /home/{current_user}/.ssh/known_hosts

# con = sshplus.SshPlus(logger)
# print(f"con: {con}")
# print(f"con debug: {con.is_debug()}")

# # for a single command on a single host
# res = con.run("uname", "10.1.1.104")

# print("RESULT:")
# print(res)
# print("Output:")
# print(res["10.1.1.104"][0][0])
# print("Errors:")
# print(res["10.1.1.104"][0][1])





"""
SCENARIO 2: TESTED: OK
	- Authenticate as the specified user with a password
	- use specific host keys file	
	- run multiple commands on a single host
"""
# # The default values if not specified explicitly:  
# SSH_USER=dev_settings.SSH_USER
# # SSH_PASSWD=None # prompts for the current user's password
# # SSH_PK_PATH=None # no rivate key auth is used
# # SSH_PK_PASS=None # no rivate key auth is used
# # SSH_HOSTKEY_AUTO_ADD=False # RejectPolicy is active
# SSH_HOSTKEY_PATH=dev_settings.SSH_HOSTKEY_PATH

# con = sshplus.SshPlus(logger, user=SSH_USER,
# 					host_keys_file_path=SSH_HOSTKEY_PATH)
# print(f"con: {con}")
# print(f"con debug: {con.is_debug()}")

# # for multiple commands on a single host
# cmds = ["uname", "ls -al",
# 		"rm ab.txt", "rmdir ximages",
# 		"rmdir dumps",
# 		"echo 'your_passwd' | sudo -S whoami",
# 		"printf '23\nmale\n' | python3 ~/z3/query.py"]

# res = con.run(cmds, "10.1.1.104")
# print("="*50) # used as a simple separator for readability 
# print("RESULT:")
# print(res)

# print("="*50) # used as a simple separator for readability 
# for cmd in res["10.1.1.104"]:
# 	print("\nOutput:")
# 	for line in cmd[0]:
# 		print("\t" + line.strip())
# 	print("\nErrors:")
# 	for line in cmd[1]:
# 		print("\t" + line.strip())





"""
SCENARIO 3: TESTED: OK
	- Authenticate as the specified user with a private key
	- use specific host keys file	
	- run multiple commands on a single host
"""
# # The default values if not specified explicitly:  
# SSH_USER=dev_settings.SSH_USER
# # SSH_PASSWD=None # prompts for the current user's password
# SSH_PK_PATH=dev_settings.SSH_PK_PATH
# SSH_PK_PASS=dev_settings.SSH_PK_PASS # set None if no passphrase required
# # SSH_HOSTKEY_AUTO_ADD=False # RejectPolicy is active
# SSH_HOSTKEY_PATH=dev_settings.SSH_HOSTKEY_PATH

# con = sshplus.SshPlus(logger, user=SSH_USER,
# 					host_keys_file_path=SSH_HOSTKEY_PATH,
# 					pk_path=SSH_PK_PATH, pk_pass=SSH_PK_PASS)
# print(f"con: {con}")
# print(f"con debug: {con.is_debug()}")

# # for multiple commands on a single host
# cmds = ["uname", "ls -al",
# 		"rm ab.txt", "rmdir ximages",
# 		"echo 'your_passwd' | sudo -S whoami",
# 		"printf '23\nmale\n' | python3 ~/z3/query.py"]

# res = con.run(cmds, "10.1.1.104")
# print("="*50) # used as a simple separator for readability 
# print("RESULT:")
# print(res)

# print("="*50) # used as a simple separator for readability 
# for cmd in res["10.1.1.104"]:
# 	print("\nOutput:")
# 	for line in cmd[0]:
# 		print("\t" + line.strip())
# 	print("\nErrors:")
# 	for line in cmd[1]:
# 		print("\t" + line.strip())





"""
SCENARIO 4: TESTED: NOPE
	- Authenticate as the specified user with a private key
	- use specific host keys file	
	- run multiple commands on multiple hosts
"""
# # The default values if not specified explicitly:  
# SSH_USER=dev_settings.SSH_USER
# # SSH_PASSWD=None # prompts for the current user's password
# SSH_PK_PATH=dev_settings.SSH_PK_PATH
# SSH_PK_PASS=dev_settings.SSH_PK_PASS # set None if no passphrase required
# # SSH_HOSTKEY_AUTO_ADD=False # RejectPolicy is active
# SSH_HOSTKEY_PATH=dev_settings.SSH_HOSTKEY_PATH

# con = sshplus.SshPlus(logger, user=SSH_USER,
# 					host_keys_file_path=SSH_HOSTKEY_PATH,
# 					pk_path=SSH_PK_PATH, pk_pass=SSH_PK_PASS)
# print(f"con: {con}")
# print(f"con debug: {con.is_debug()}")

# # for multiple commands on a single host
# cmds = ["hostname", "ls -al",
# 		# "echo 'your_passwd' | sudo -S whoami",
# 	# "pritf '23\nmale\n' | python3 ~/z3/query.py"]
# ]

# devices = ["10.1.1.104", "10.1.1.125", "10.1.1.100"]

# res = con.run(cmds, devices)
# print("="*50) # used as a simple separator for readability 
# print("RESULT:")
# print(res)
# # print("="*50) # used as a simple separator for readability 
# # print(res.keys())
# # print(k for k in res.items())
# # print(res['10.1.1.125'][0][0])
# # print(res['10.1.1.125'][0][1])

# # print("="*50) # used as a simple separator for readability 
# # for k,v in res.items():
# # 	for cmd in v:
# # 		print("\nOutput:")
# # 		for line in cmd[0]:
# # 			print("\t" + line.strip())
# # 		print("\nErrors:")
# # 		for line in cmd[1]:
# # 			print("\t" + line.strip())
# # 	print("-"*50) # used as a simple separator for readability

