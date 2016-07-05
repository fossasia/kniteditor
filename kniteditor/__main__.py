"""The main program of the editor.

This file starts the editor window.
"""
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from kniteditor.EditorWindow import main
    main()
