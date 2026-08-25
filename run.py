"""Start the app. In PyCharm: right-click this file, Run.

Host and port come from .env (APP_HOST / APP_PORT). Set APP_HOST=0.0.0.0 to
reach it from your phone on the same wifi.
"""

from wardrobe.app import main

if __name__ == "__main__":
    main()
