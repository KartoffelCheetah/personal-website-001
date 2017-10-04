#! /usr/bin/python3
"""You can run here the database_operations or anything really.
Just select the proper import statement"""

if __name__=='__main__':
    import sys
    green = '\x1b[32m'
    normal = '\x1b[0m'
    red = '\x1b[31m'

    print("""
    For more info use help('main) in the python console.

    0: exit
    1: Create database
    2: Populate photos
    3: Populate drawings
    anything else will exit
    """)
    try:
        op = int(input("select the database operation's id: "))
    except:
        op = 0

    try:
        if op == 0:
            sys.exit(green+'exit'+normal)
        elif op == 1:
            print(green, 'creating database...', normal)
            from db import create_db
            create_db()
        elif op == 2:
            print(green, 'populating photos...', normal)
            import database_operations.populate_photos
        elif op == 3:
            print(green, 'populating drawings...', normal)
            import database_operations.populate_drawings
        else:
            sys.exit(green+'exit'+normal)
        # being here means total success
        print(green, 'Finished operation!', normal)
    except Exception as e:
        # in case of error print the error in red
        print(red, e, normal)
        print(red, 'Finished operation!', normal)
