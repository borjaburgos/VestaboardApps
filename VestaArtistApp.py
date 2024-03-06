import requests
import os
import sys
import ast
import pprint
from vestaboard import Board
from openai import OpenAI
from unidecode import unidecode


# Step 1: Get User Prompt
def get_artist():
	if len(sys.argv) > 1:
		return sys.argv[1]
	else:
		return "creative"
	
# Step 2: Generate a Message with ChatGPT
def generate_message(artist):
	client = OpenAI()
	while True:
		response = client.chat.completions.create(
			model="gpt-4-0125-preview",
			messages=[
				{"role": "system", "content": "Generate a 6 pixel by 22 pixel image using the following color codes: Red (63), Orange (64), Yellow (65), Green (66), Blue (67), Violet (68), White (69), Black (70). The only output should be the art in a 6 row by 22 column array delimited by brackets."},
				{"role": "user", "content": f"Display {artist}"},
			],
			# temperature=0.7,
			max_tokens=600
		)
		pprint.pprint(response)
		# Get array from OpenAI Response
		cleaned_response = response.choices[0].message.content.strip('` \n')
		rows = cleaned_response.split('\n')
		array = [list(map(int, row.strip('[]').replace(', ', ',').split(','))) for row in rows]
		
		if isinstance(array, list) and len(array) == 6 and all(len(row) == 22 for row in array):
			return array
		else:
			print("Generated array does not meet the required dimensions. Retrying...")
	
# Step 3: Display the Message on Vestaboard
def display_on_vestaboard(array):
	print(array)
	vestaboard_api_key = os.environ.get("VESTABOARD_API_KEY")
	vestaboard_ip = os.getenv("VESTABOARD_IP_ADDRESS", "vestaboard.local")
	localBoard = Board(localApi={ 'ip': vestaboard_ip, 'key': vestaboard_api_key})	
 	localBoard.raw(array)
	
# Step 4: Print to console
def print_colored_array(array):
	color_codes = {
		63: "\033[31m",  # Red
		64: "\033[33m",  # Orange
		65: "\033[93m",  # Yellow
		66: "\033[32m",  # Green
		67: "\033[34m",  # Blue
		68: "\033[35m",  # Violet
		69: "\033[97m",  # White
		70: "\033[30m",  # Black
	}
	
	for row in array:
		for value in row:
			print(f"{color_codes.get(value, '')}■", end="")
		print("\033[0m")  # Reset color
	
# Main function
def main():
	
	# Check if VESTABOARD_API_KEY is defined
	if 'VESTABOARD_API_KEY' not in os.environ:
		raise ValueError("VESTABOARD_API_KEY environment variable is not defined")
	
	# Check if OPENAI_API_KEY is defined
	if 'OPENAI_API_KEY' not in os.environ:
		raise ValueError("OPENAI_API_KEY environment variable is not defined")
	
	artist = get_artist()
	visual_array = generate_message(artist)
	display_on_vestaboard(visual_array)
	print_colored_array(visual_array)
	
if __name__ == "__main__":
	main()
