#! /usr/bin/python3.5
"""This file is to run frequently used scripts.
Just select the proper operation number to run it."""

if __name__=='__main__':
    import sys, os, json, subprocess
    from os.path import join as pathJoin
    from server import STAGING_AREA
    from server import app, DATABASE, DRAWINGS, PHOTOS, FULL_IMAGES, FULL_THUMBNAILS
    from db import create_db, drawings, photos, photosDict, drawingsDict
    from db import insert_photo, insert_drawing
    from db import select_all_photos, select_all_drawings
    from db import print_table, dict_from_row
    from IMfunctions import *
    from console_paint_presets import *
    # green = '\x1b[32m'
    # yellow = '\x1b[33m'
    # normal = '\x1b[0m'
    # red = '\x1b[31m'
    # magenta = '\x1b[35m'

    print("""
    For more info use help('main') in the python console.

    0: exit
    1: Create database
    2: Create Staging file
    3: Use Staging file
    4: Print Size of images
    5: Select all images
    6: Create Staging file from db
    7: Delete database
    anything else will exit
    """)
    try:
        op = int(input("select the operation's id: "))
    except:
        op = 0

    try:
        if   op == 0 :
            # sys.exit(green+'exit'+normal)
            printOK('exit')
            sys.exit('Bye!')
        elif op == 1 :
            # print(green, 'creating database...', normal)
            printOK('creating database...')
            create_db()
        elif op == 2 :
            staged_files = []
            for dirpath, dirnames, filenames in os.walk(STAGING_AREA) :
                for filename in filenames :
                    if not filename.endswith('.json'):
                        shortened_path = (dirpath
                            .replace(STAGING_AREA+'/'+PHOTOS.rstrip('/'),'')
                            .replace(STAGING_AREA+'/'+DRAWINGS.rstrip('/'),'')
                            .replace(STAGING_AREA, '')
                            .lstrip('/'))
                        default_url = pathJoin(shortened_path, filename)
                        default_title = os.path.splitext(filename)[0]
                        default_table_type = 'drawings' if 'drawings' in dirpath else 'photos'
                        default_createDate = getDateTimeOriginal(pathJoin(dirpath,filename)).replace(':','-', 2)
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
                with open(pathJoin(STAGING_AREA,'staging.json'), 'w') as staging_file:
                    print('Overwriting staging file...')
                    json.dump(staged_files, staging_file, indent=2)
                print('Finished dumping. Staging file is done.')
                # print(yellow+'Please check the staging file before uploading to database.\nDo not forget to order the elements in the list and fill out the descriptions.'+normal)
                printWarning('Please check the staging file before uploading to database.\nDo not forget to order the elements in the list and fill out the descriptions.')
            else:
                print('Aborting... Kept staging file.')
        elif op == 3 :
            # TODO: staged_url, thumb_url, and their temp versions declared too many times
            with open(pathJoin(STAGING_AREA,'staging.json')) as staging_file:
                staged_files = json.loads(staging_file.read())
                staged_drawings = [sf for sf in staged_files if sf['tableType']=='drawings']
                staged_photos = [sf for sf in staged_files if sf['tableType']=='photos']
                drawings.execute('BEGIN')
                for sd in staged_drawings:
                    insert_drawing(**sd)
                drawings.execute('COMMIT')
                for sd in staged_drawings:
                    # base image location
                    staged_url = pathJoin(STAGING_AREA,DRAWINGS,sd['url'])
                    # thumbnail image location
                    thumb_url = pathJoin(FULL_THUMBNAILS,DRAWINGS,sd['url'])
                    # public image location
                    public_url = pathJoin(FULL_IMAGES,DRAWINGS,sd['url'])
                    # temporary thumbnail image location
                    temp_thumb_url = thumb_url + '_tmp'
                    # temporary image location
                    temp_url = public_url + '_tmp'

                    os.rename(temp_thumb_url, thumb_url)
                    os.rename(temp_url, public_url)
                    # os.remove(staged_url)
                print('Drawings are live now.')
                photos.execute('BEGIN')
                for sp in staged_photos:
                    insert_photo(**sp)
                photos.execute('COMMIT')
                for sf in staged_photos:
                    # base image location
                    staged_url = pathJoin(STAGING_AREA,PHOTOS,sf['url'])
                    # thumbnail image location
                    thumb_url = pathJoin(FULL_THUMBNAILS,PHOTOS,sf['url'])
                    # public image location
                    public_url = pathJoin(FULL_IMAGES,PHOTOS,sf['url'])
                    # temporary thumbnail image location
                    temp_thumb_url = thumb_url + '_tmp'
                    # temporary image location
                    temp_url = public_url + '_tmp'

                    os.rename(temp_thumb_url, thumb_url)
                    os.rename(temp_url, public_url)
                    # os.remove(staged_url)
                print('Photos are live now.')
        elif op == 4 :
            size_of_drawings = subprocess.check_output(
                ['du', '-sh', pathJoin(FULL_IMAGES, DRAWINGS)]
            ).split()[0].decode('utf-8')
            size_of_photos = subprocess.check_output(
                ['du', '-sh', pathJoin(FULL_IMAGES, PHOTOS)]
            ).split()[0].decode('utf-8')
            size_of_database = subprocess.check_output(
                ['du', '-sh', DATABASE]
            ).split()[0].decode('utf-8')
            # print(yellow+'Size of directories:\n drawings: {}\n photos: {}\n database: {}'.format(size_of_drawings,size_of_photos,size_of_database)+normal)
            printWarning(
                'Size of directories:\n drawings: {}\n photos: {}\n database: {}'.format(size_of_drawings,size_of_photos,size_of_database))
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
            with open(pathJoin(STAGING_AREA,'staging.json'), 'w') as staging_file:
                print('Overwriting staging file...')
                staging_file.write(j)
        elif op == 7 :
            if input('Are you sure you want to delete db? (yes/y): ') in ('yes', 'y') :
                os.rename(DATABASE, DATABASE+'old')
                print('DB renamed to', DATABASE+'old', '(atomic operation)')
            else:
                print('Aborting...')
        else:
            # sys.exit(green+'exit'+normal)
            printOK('exit')
            sys.exit('Unknown operation number.')
        # being here means total success
        # print(green, 'Finished operation!', normal)
        printOK('Finished operation!')
    except Exception as e:
        # in case of error print the error in red
        # print(red, e, normal)
        printAlert(e)
        # print(red, 'Finished operation!', normal)
        printAlert('Finished operation!')
        raise e
