import sys


def main():
    from kniteditor import main
    main()

if len(sys.argv) == 1:
    try:
        main()
    except:
        import traceback
        traceback.print_exc()
        while 1:
            try:
                exec(input(">>> "))
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                traceback.print_exc()
else:
    main()
