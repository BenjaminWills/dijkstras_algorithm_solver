save_requirements:
	mkdir -p requirements
	pip freeze > requirements/requirements.txt
	conda env export > requirements/conda_recipie.yml