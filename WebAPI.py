# webapi.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Henry Hanlin Zheng
# hhzheng1@uci.edu
# 19204536

import urllib.request
import urllib.error
import json
from abc import ABC, abstractmethod

class WebAPI(ABC):

	def __init__(self):
		self.set_apikey = None

	def _download_url(self, url: str) -> dict:
		#TODO: Implement web api request code in a way that supports
		# all types of web APIs
		response = None
		try:
			response = urllib.request.urlopen(url)
			data = response.read()
			return json.loads(data)

		except urllib.error.HTTPError as e:
				raise Exception(f"Remote API unavailable (HTTP Error {e.code})") from e
		except urllib.error.URLError as e:
				raise Exception("Loss of local connection to the Internet") from e
		except json.JSONDecodeError as e:
				raise Exception("Invalid data formatting from the remote API") from e
		finally:
			if response is not None:
				response.close()

	def set_apikey(self, apikey:str) -> None:
		self.apikey = apikey

	@abstractmethod
	def load_data(self):
		pass

	@abstractmethod
	def transclude(self, message:str) -> str:
		pass