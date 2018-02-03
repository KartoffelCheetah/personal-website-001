#! /usr/bin/python3
"""This file is to run frequently used scripts.
Just select the proper operation number to run it."""

if __name__=='__main__':
    import sys, os, re, json, subprocess
    from PIL import Image
    from server import STAGING_AREA as staging_area
    from server import app, DATABASE, DRAWINGS, PHOTOS
    from db import create_db, drawings, photos, photosDict, drawingsDict
    from db import insert_photo, insert_drawing
    from db import select_all_photos, select_all_drawings, print_table, dict_from_row
    green = '\x1b[32m'
    yellow = '\x1b[33m'
    normal = '\x1b[0m'
    red = '\x1b[31m'
    magenta = '\x1b[35m'

    print("""
    For more info use help('main') in the python console.

    0: exit
    1: Create database
    2: Create Staging file
    3: Use Staging file
    4: Print Size of images
    5: Select all images
    6: Create Staging file from db
    anything else will exit
    """)
    try:
        op = int(input("select the operation's id: "))
    except:
        op = 0

    try:
        if   op == 0 :
            sys.exit(green+'exit'+normal)
        elif op == 1 :
            print(green, 'creating database...', normal)
            create_db()
        elif op == 2 :
            staged_files = []
            for dirpath, dirnames, filenames in os.walk(staging_area) :
                for filename in filenames :
                    if not filename.endswith('.json'):
                        shortened_path = (dirpath
                        .replace(staging_area+'/', '')
                        .replace(staging_area+'\\', '')
                        .replace(staging_area, ''))
                        path_to_url = '/'.join(['/img', shortened_path, filename])
                        default_url = re.sub(r'/+', '/', path_to_url)
                        default_title = os.path.splitext(filename)[0]
                        default_table_type = 'drawings' if 'drawings' in dirpath else 'photos'
                        try:
                            default_createDate = Image.open(os.path.join(dirpath,filename))._getexif()[36867].replace(':','-', 2)
                        except AttributeError:
                            default_createDate = None
                        staged_files.append({
                            'url':default_url,
                            'title':default_title,
                            'desc':'',
                            'createDate':default_createDate,
                            'license':None,
                            'tableType': default_table_type
                        })
            clear_staging = input('I need to overwrite the staging file. Are you okay with this? (yes/y): ').lower() in ('yes', 'y')
            if clear_staging:
                with open(os.path.join(staging_area,'staging.json'), 'w') as staging_file:
                    print('Overwriting staging file...')
                    json.dump(staged_files, staging_file, indent=2)
                print('Finished dumping. Staging file is done.')
                print(yellow+'Please check the staging file before uploading to database.\nDo not forget to order the elements in the list and fill out the descriptions.'+normal)
            else:
                print('Aborting... Kept staging file.')
        elif op == 3 :
            with open(os.path.join(staging_area,'staging.json')) as staging_file:
                staged_files = json.loads(staging_file.read())
                staged_drawings = [sf for sf in staged_files if sf['tableType']=='drawings']
                staged_photos = [sf for sf in staged_files if sf['tableType']=='photos']
                drawings.execute('BEGIN')
                for sd in staged_drawings:
                    insert_drawing(**sd)
                drawings.execute('COMMIT')
                for sd in staged_drawings:
                    staged_url = staging_area+sd['url'].replace('/img','',1)
                    public_url = app.static_folder+sd['url']
                    if not os.path.exists(os.path.split(public_url)[0]):
                        os.makedirs(os.path.split(public_url)[0])
                    os.rename(staged_url, public_url)
                print('Drawings are live now.')
                photos.execute('BEGIN')
                for sp in staged_photos:
                    insert_photo(**sp)
                photos.execute('COMMIT')
                for sf in staged_photos:
                    staged_url = staging_area+sf['url'].replace('/img','',1)
                    public_url = app.static_folder+sf['url']
                    if not os.path.exists(os.path.split(public_url)[0]):
                        os.makedirs(os.path.split(public_url)[0])
                    os.rename(staged_url, public_url)
                print('Photos are live now.')
        elif op == 4 :
            size_of_drawings = subprocess.check_output(
                ['du', '-sh', os.path.join(app.static_folder, DRAWINGS)]
            ).split()[0].decode('utf-8')
            size_of_photos = subprocess.check_output(
                ['du', '-sh', os.path.join(app.static_folder, PHOTOS)]
            ).split()[0].decode('utf-8')
            size_of_database = subprocess.check_output(
                ['du', '-sh', DATABASE]
            ).split()[0].decode('utf-8')
            print(yellow+'Size of directories:\n drawings: {}\n photos: {}\n database: {}'.format(size_of_drawings,size_of_photos,size_of_database)+normal)
        elif op == 5 :
            selected_drawings = select_all_drawings(drawingsDict)
            selected_photos = select_all_photos(photosDict)
            print('DRAWINGS ˇ')
            print_table(selected_drawings)
            print('PHOTOS ˇ')
            print_table(selected_photos)
        elif op == 6 :
            selected_drawings = dict_from_row(select_all_drawings(drawingsDict))
            selected_photos = dict_from_row(select_all_photos(photosDict))
            for i in selected_drawings:
                i.update({'tableType':'drawings'})
            for i in selected_photos:
                i.update({'tableType':'photos'})
            j = (json.dumps(selected_photos+selected_drawings, indent=2)
            .replace('\"datetimeoriginal\":', '\"createDate\":')
            .replace('\"description\":', '\"desc\":'))
            print(j)
            clear_staging = input('I need to overwrite the staging file. Are you okay with this? (yes/y): ').lower() in ('yes', 'y')
            if not clear_staging:
                sys.exit('Aborting... Kept staging file.')
            with open(os.path.join(staging_area,'staging.json'), 'w') as staging_file:
                print('Overwriting staging file...')
                staging_file.write(j)
        else:
            sys.exit(green+'exit'+normal)
        # being here means total success
        print(green, 'Finished operation!', normal)
    except Exception as e:
        # in case of error print the error in red
        print(red, e, normal)
        print(red, 'Finished operation!', normal)
