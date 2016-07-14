try:
    from kniteditor import main
    main()
except:
    import traceback
    traceback.print_exc()
    while 1:
        try:
            exec(input(">>> "))
        except:
            traceback.print_exc()
