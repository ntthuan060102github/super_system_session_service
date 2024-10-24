install_pkg:
	pip uninstall -y pkg-helpers
	pip uninstall -y pkg-libs
	pip install -r requirements.txt