import requests
import os
from vestaboard import Board
from openai import OpenAI
from unidecode import unidecode

# Step 1: Retrieve Local Weather Data
def get_weather(zip_code):
	api_key = os.environ.get('WEATHER_API_KEY')
	url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={zip_code}&lang=es"
	response = requests.get(url)
	data = response.json()
	condition = data["current"]["condition"]["text"]
	temp_c = data["current"]["temp_c"]
	print(response.json()['location']['localtime'])
	return response.json()
	
# Step 2: Generate a Message with ChatGPT
def generate_message(weather):
	client = OpenAI()
	response = client.chat.completions.create(
		model="gpt-4-0125-preview",
		messages=[
			{"role": "system", "content": "You are a helpful assistant. Your response must be 132 characters or less, including spaces."},
			{"role": "user", "content": f"Write a simple and short message in Spanish (from Spain/Argentina) about the day's weather forecast for a 6-year-old child who is learning to read. It is important to highlight whether it will rain throughout the day or not. . Today's forecast is: {weather}"},
		],
		temperature=0.7,
		max_tokens=60
	)
	return response.choices[0].message.content
	
# Step 3: Display the Message on Vestaboard
def display_on_vestaboard(message):
	print(message)
	print(unidecode(message))
	vestaboard_api_key = os.environ.get("VESTABOARD_API_KEY")
	vestaboard_ip = os.getenv("VESTABOARD_IP_ADDRESS", "vestaboard.local")
	localBoard = Board(localApi={ 'ip': vestaboard_ip, 'key': vestaboard_api_key})
	localBoard.post(unidecode(message)) # ensures no unsupported characters are passed to the vestaboard
	
# Main function
def main():
	
	# Check if WEATHER_API_KEY is defined
	if 'WEATHER_API_KEY' not in os.environ:
		raise ValueError("WEATHER_API_KEY environment variable is not defined")
	
	# Check if VESTABOARD_API_KEY is defined
	if 'VESTABOARD_API_KEY' not in os.environ:
		raise ValueError("VESTABOARD_API_KEY environment variable is not defined")
	
	# Check if OPENAI_API_KEY is defined
	if 'OPENAI_API_KEY' not in os.environ:
		raise ValueError("OPENAI_API_KEY environment variable is not defined")
	
	# Set ZIP_CODE to Washington DC's ZIP Code if not defined
	zip_code = os.environ.get('ZIP_CODE', '20001')
	
	weather = get_weather(zip_code)
	message = generate_message(weather)
	display_on_vestaboard(message)
	
if __name__ == "__main__":
	main()
