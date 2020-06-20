# Developed by A N Zeyn

import time
import os
import sys
import paramiko
import getpass


class SshPlus:
	"""
	SshPlus allows to:
		- connect over ssh to one or more devices at the same time
		- run single or multiple commands on the target devices(s)
	"""

	DEBUG = False

	def __init__(self, logger, *args, **kwargs):

		self.logger = logger

		if kwargs.get('debug'):
			SshPlus.DEBUG = kwargs.get('debug')
		if SshPlus.DEBUG:
			self.logger.log_plus("pld", f"DEBUG: {SshPlus.DEBUG}")

		self.user = kwargs.get('user') or getpass.getuser()
		self.passwd=None
		self.prv_key = None
		self.pk_path = kwargs.get('pk_path') or None
		self.pk_pass = kwargs.get('pk_pass') or None
		self.host_keys_file_path = kwargs.get('host_keys_file_path') or None
		self.host_keys_auto_add = kwargs.get('host_keys_auto_add') or False
		self.display = kwargs.get('display') or False

		if SshPlus.DEBUG:
			self.logger.log_plus("pld", f"self.display: {self.display}")

		if not self.pk_path:
			self.passwd = kwargs.get('passwd') or getpass.getpass("Password: ")
			if not self.passwd:
				self.logger.log_plus("plex", "Not all necessary credentials have been provided")
		else:
			self.prv_key = self.set_private_key()
		
		self.connect()
		if SshPlus.DEBUG:
			self.logger.log_plus("pld", f"Initial self.connect: {self.connect}")
		
		self.logger.log_plus("pli", "SshPlus instance has been created successfully")

	def set_private_key(self):
		try:
			self.prv_key = paramiko.RSAKey.from_private_key_file(self.pk_path, self.pk_pass)
			return self.prv_key
		except FileNotFoundError as fnfe:
			self.logger.log_plus("plex", f"The private key file path is wrong or does not exist. \n {fnfe}")
		except paramiko.ssh_exception.SSHException as ssh_e:
			self.logger.log_plus("plex", f"{ssh_e}\nThe private key file passphrase might be wrong or not provided.")
		except Exception as e:
			self.logger.log_plus("plex", f"{e}\nSomething went wrong. Review your settings for correctness!")

	def connect(self):
		self.client = paramiko.SSHClient()
		self.set_host_keys()
	
	def set_host_keys(self):		
		if self.host_keys_auto_add:
			self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			#Vulnerable to MITM attacks. OR be more specific:
			if SshPlus.DEBUG:
				self.logger.log_plus("pld", f"Missing HostKey AutoAdd: {self.host_keys_auto_add}")
		else:
			self.client.set_missing_host_key_policy(paramiko.RejectPolicy())
			if SshPlus.DEBUG:
				self.logger.log_plus("pld", f"Missing HostKey AutoAdd: {self.host_keys_auto_add}")

		if self.host_keys_file_path:
			try:			
				self.client.load_host_keys(self.host_keys_file_path)
				if SshPlus.DEBUG:
					self.logger.log_plus("pld", f"HostKeyInUse: {self.host_keys_file_path}")
				return self.client
			except FileNotFoundError as fnfe:
				fnfe_msg = """
	Check the correctness of the host key file path that you specified.
	Ensure the file actually exists and you have necessary access permissions.
				"""
				self.logger.log_plus("plex", f"Error: {fnfe}{fnfe_msg}")
			except Exception as e:
				self.logger.log_plus("plex", f"Error: {e}")
		else:
			try:
				self.client.load_host_keys(os.path.expanduser(f"/home/{self.user}/.ssh/known_hosts"))
				if SshPlus.DEBUG:
					self.logger.log_plus("pld", f"HostKeyInUse: /home/{self.user}/.ssh/known_hosts")
				return self.client
			except FileNotFoundError as fnfe:
				fnfe_msg = """
	Ensure the local hosts key file actually exists and you have necessary access permissions.
				"""
				self.logger.log_plus("plex", f"Error: {fnfe}{fnfe_msg}")
			except Exception as e:
				self.logger.log_plus("plex", f"Error: {e}")

	def validate(self, cmd_or_device_list):
		if isinstance(cmd_or_device_list, str):
			if SshPlus.DEBUG:
				self.logger.log_plus("pld", f"{cmd_or_device_list} is valid")
			return [cmd_or_device_list]
		elif isinstance(cmd_or_device_list, (list, tuple)):
			if SshPlus.DEBUG:
				self.logger.log_plus("pld", f"{cmd_or_device_list} is valid")
			return cmd_or_device_list
		else:
			self.logger.log_plus("plex", f"{cmd_or_device_list} is invalid")

	def execute_from_cmd_list(self):
		# return: cmd_data
		# ((res_1, res_1_err),..., (res_n, res_n_err))}
		cmd_data = list()
		for i, cmd in enumerate(self.cmd_list):
			stdin , stdout, stderr = self.client.exec_command(cmd, get_pty=True)
			response = stdout.readlines()
			response_err = stderr.readlines()
			response_pair = (response, response_err)
			cmd_data.append(response_pair)
			if self.display:
				if response:
					self.logger.log_plus("pli", f"Raw Response Data: {response}")
					for line in response:
						self.logger.log_plus("pli", f"{line.strip()}")		
				if response_err:
					self.logger.log_plus("pli", f"Raw Response Error: {response_err}")
		return tuple(cmd_data)
			

	def run(self, cmd_list, device_list):
		# return_data
		# {
		# 	"device_name_ip_1": ((res_1, res_1_err),..., (res_n, res_n_err)),
		# 			.	.	.	.	.
		# 	"device_name_ip_n": ((res_1, res_1_err),..., (res_n, res_n_err)),
		# }
		return_data = dict()
		self.cmd_list = self.validate(cmd_list)
		self.device_list = self.validate(device_list)

		if self.prv_key:
			for device in self.device_list:
				if SshPlus.DEBUG:
					self.logger.log_plus("pld", f"prv_key conenct to {device}")
					self.logger.log_plus("pld", f"self client: {self.client}")
					self.logger.log_plus("pld", f"self user: {self.user}")
				try:
					self.client.connect(hostname=device, username=self.user, pkey=self.prv_key)
					self.logger.log_plus("pli", f"{device}: Connected")
					return_data[device] = self.execute_from_cmd_list()
				except paramiko.ssh_exception.NoValidConnectionsError as not_connect:
					self.logger.log_plus("ple", f"{device}: Unable to connect")
					self.logger.log_plus("ple", f"\tConnection Error: {not_connect}")
				except paramiko.ssh_exception.AuthenticationException as auth_e:
					self.logger.log_plus("ple", f"Authentication Error: {auth_e}")
				except Exception as e:
					self.logger.log_plus("ple", f"Error: {e}")

		elif self.passwd:
			for device in self.device_list:
				if SshPlus.DEBUG:
					self.logger.log_plus("pld", f"passwd conenct to {device}")
					self.logger.log_plus("pld", f"self client: {self.client}")
					self.logger.log_plus("pld", f"self user: {self.user}")
				try:
					self.client.connect(hostname=device, username=self.user, password=self.passwd)
					self.logger.log_plus("pli", f"{device}: Connected")
					return_data[device] = self.execute_from_cmd_list()
				except paramiko.ssh_exception.NoValidConnectionsError as not_connect:
					self.logger.log_plus("ple", f"{device}: Unable to connect")
					self.logger.log_plus("ple", f"\tConnection Error: {not_connect}")
				except paramiko.ssh_exception.AuthenticationException as auth_e:
					self.logger.log_plus("ple", f"Authentication Error: {auth_e}")
				except Exception as e:
					self.logger.log_plus("ple", f"Error: {e}")


		self.client.close()
		return return_data
		

	@classmethod
	def is_debug(cls):
		return cls.DEBUG



