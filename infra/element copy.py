import glob

dirs = ['NON-a', '9月7日 佐藤*/*404', '9月7日 佐藤*/*537', '9月8日 佐藤*/*117,9月8日 佐藤*/*253']
pattern = '9月7日 佐藤*/*396.JPG'

for directory in dirs:
    file_paths = glob.glob(directory + '/' + pattern.replace('*', '\\*'))
    
    for file_path in file_paths:
        print(file_path)