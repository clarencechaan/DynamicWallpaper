# nohup python DynamicWallpaper.py {s,u,a,d} value interval [-n] &
# exit

import os, flickr_api, time, argparse, itertools
FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/"
flickr_api.set_keys(api_key='ea4fe53256c484c33bba136f5343446a', api_secret='3f5493403e640057')

# in a loop, change wallpaper given a list of photos, for s,u,a only
def loop_change(photos, new_only, interval):
    if new_only:
        for p in photos:
            print(p)
            if not os.path.exists(FILE_PATH + p.id):
                p.save(p.id)
                os.system("gsettings set org.gnome.desktop.background picture-uri file://" + FILE_PATH + p.id)
                time.sleep(interval)
    else:
        for p in photos:
            print(p)
            if not os.path.exists(FILE_PATH + p.id):
                p.save(p.id)
            os.system("gsettings set org.gnome.desktop.background picture-uri file://" + FILE_PATH + p.id)
            time.sleep(interval)

# return a list of photos given search option and term
def get_photos_by_option(option, term):
    if option == "s":
        # try "minimalism"  
        print("Searching for photos with tag \"" + term + "\"")
        return flickr_api.Walker(flickr_api.Photo.search, tags=term)
    elif option == "u":
        # try "alexcurrie"
        print("Retrieving photos from user " + term)
        user = flickr_api.Person.findByUserName(term)
        return user.getPublicPhotos()
    elif option == "a":
        # try "72157669309212490"
        print("Retrieving photos from album with ID " + term)
        photoset = flickr_api.Photoset(id=term)
        return photoset.getPhotos()

def change_by_directory(directory, interval):
    # try ~/Pictures/
    for filename in itertools.cycle(os.listdir(directory)):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            print(os.path.join(directory, filename))
            os.system("gsettings set org.gnome.desktop.background picture-uri \"file://"
                      + os.path.join(directory, filename) + "\"")
            time.sleep(interval)

def start(option, value, interval, flag_new):
    print("Changing wallpaper every " + str(interval) + " seconds.")

    photos = []
    if option == "d":
        change_by_directory(value, interval)
    else:
        photos = get_photos_by_option(option, value)

    loop_change(photos, flag_new, interval)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("option", help="retrieve photos by search, user, album ID, or directory", choices=["s", "u", "a", "d"])
    parser.add_argument("value", help="input search term, username, album ID, or directory")
    parser.add_argument("interval", type=int, help="number of seconds between each wallpaper change")
    parser.add_argument("-n", "--new", help="new photos only", action="store_true")
    args = parser.parse_args()

    start(args.option, args.value, args.interval, args.new)