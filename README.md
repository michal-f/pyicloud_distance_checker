# Python iCloud location checker

### DISTANCE CHECKER BETWEEN DEVICE AND SELECTED POINT via ICLOUD SERVICE

## info:

outputs console logs and sound notifications about iCloud device movement.

control and track distance between iCloud connected device and source location.



## Requirements:
Most reuirements are in repo, but mayby not all.

Full requirements pip file comes soon... 


## How run app?
  1. Create file "login_credentials.txt" in root location with iCloud login credentials in such format:
    
    ```
    login:password
    ```
    
  example:
    
    ```
    michal.f@mail.com:Password
    ```
    
  2. Get source location cordinantes (from any map or something examplegoogle maps)
    
  Edit settings.py file and provide your source location cordinantes:
    
    ```
    SOURCE_LOCATION_CORDINANTES = {
        'latitude': 54.503501,
        'longitude': 18.542396
    }
    
    ```

  3. run in console:

    ```
    python checker.py
    ```

## Development status

This is a development in progress pre alfa release.

Basic functionality is working but there is many possible work to do :)

- actually console logs and sound notifications 
- currently developing frontview (Pygame display and control panel) code comes soon...

...
its a open source private project
for questions contact me: michal.f@mail.com Michal Frackowiak

