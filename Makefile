ENTRYPOINT_PATH=ark_nova-setup_randomizer/frontend/entrypoint.py
DOCKER_IMAGE=ark_nova-setup_randomizer

build_docker:
	docker build . -t $(DOCKER_IMAGE)

run_docker:
	docker run -p 8501:8501 --rm $(DOCKER_IMAGE):latest

build_and_run_docker: build_docker run_docker

run_locally:
	streamlit run $(ENTRYPOINT_PATH) --server.port=8501 --server.address=0.0.0.0
