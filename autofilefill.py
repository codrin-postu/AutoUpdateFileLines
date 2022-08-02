import os
import sys


def read_file(file_path: str):
    """Function reads the file and returns all the lines in a list.
    Each line has the newline removed.

    Args:
        file_path (str): Path of the file that will be opened.

    Returns:
        list: List of lines that were read from the file
    """
    f = open(file_path, encoding='utf-8')
    lines = f.readlines()
    f.close()

    return [line.rstrip() for line in lines]


def write_in_file(file_path: str, lines: list):
    """Writes the new lines and the old sorted lines (if the case) in
    the specified file path.

    Args:
        file_path (str): Path of the file that will be opened.
        lines (list): List of lines to be added
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(f"{line}\n")


def update_lines(file_lines: list, lines_to_add: list):
    """Removes duplicate entries in the file and adds the specified lines

    Args:
        file_lines (list): Lines that exist in the file 
        lines_to_add (list): Lines that should be added to the file

    Returns:
        list: List of all the new lines to be added in the file
    """
    for line in file_lines:
        split_line = line.split('|')
        if any(split_line[0] in l for l in lines_to_add):
            file_lines.remove(line)

    file_lines.extend(lines_to_add)
    return file_lines


def update_files(rootdir: str, filename: str, to_sort: bool, lines_to_add: list):
    """Searches in the specified directory for files with the specified 
    filename and adds the new lines.

    Args:
        rootdir (str): The path to the root directory
        filename (str): Name of the file which should be modified
        to_sort (bool): Specifies whether the lines in the file should be sorted alphabetically
        lines_to_add (list): List of lines to be added in the file
    """
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file != filename:
                continue

            file_path = os.path.join(subdir, file)

            file_lines = read_file(file_path)

            file_lines = update_lines(file_lines, lines_to_add)

            if to_sort:
                file_lines.sort()

            write_in_file(file_path, file_lines)

            file_lines.clear()


def get_necessary_data(argv: list):
    """Gets the necessary data to run the script

    Args:
        argv (list): Arguments added when running the script
    """
    lines_to_add = []

    if len(argv) <= 1:
        print("autofilefill.py <root_dir_path> <file_name>")
        rootdir = input('Insert root directory to search for files: ')
        filename = input('Insert file name (including extension): ')
    else:
        rootdir = argv[0]
        filename = argv[1]

    sort_input = input(
        'Would you like the files to be sorted?\nOtherwise new lines will be added at the end of the files (Y/N): ')
    to_sort = sort_input.upper() == 'Y'

    print("Add all the lines you wish. Send empty string to finish.")
    while True:
        new_line = input("New line: ")
        if new_line == '':
            break
        lines_to_add.append(new_line)

    update_files(rootdir, filename, to_sort, lines_to_add)


if __name__ == "__main__":
    get_necessary_data(sys.argv[1:])
