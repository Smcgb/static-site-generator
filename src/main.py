import os
import shutil

def recursive_copy(source: str, destination: str) -> None: 

	# This can be more easily done with copytree or shutil move. This was a requirement from the program to make my own recursive move.

	if not os.path.exists(source):
		raise FileNotFoundError(f"source does not exist: {source}")
	if not os.path.exists(destination):
		os.mkdir(destination)

	for item in os.listdir(source):
		path = f"{source}/{item}"
		if os.path.isdir(path):
			recursive_copy(path, f"{destination}/{item}")
		else:
			print(f"Copying {path} to {destination}")
			shutil.copy2(path, destination)

def clean_folder(folder: str) -> None:

	if os.path.exists(folder):
		shutil.rmtree(folder)
	

def main():

	clean_folder("public")
	recursive_copy("static", "public")

if __name__ == "__main__":
    main()
