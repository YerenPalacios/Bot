i:
	pip install -r requirements.txt

r:
	python main.py

serve:
	uvicorn api.py