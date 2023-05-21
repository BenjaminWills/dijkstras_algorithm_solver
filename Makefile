save_requirements:
	mkdir -p requirements
	pip freeze > requirements/requirements.txt
	conda env export > requirements/conda_recipie.yml

start_gui:
	python gui/graphing_gui.py

open_example:
	open ./non_gui_example.ipynb