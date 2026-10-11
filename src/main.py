from recurisve_copy import clean_folder, recursive_copy


def main():

	clean_folder("public")
	recursive_copy("static", "public")

if __name__ == "__main__":
    main()
