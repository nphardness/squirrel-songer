# squirrel-songer

Song list / repertoire manager for twitch!


## Development

1. Create virtualenv and activate it:

    $ virtualenv -p python3 .venv
    $ source .venv/bin/activate

2. Install requirements and run db migrations:

    $ pip install -r requirements.txt
    $ python manage.py migrate

3. Run:

    $ python manage.py runserver 8000

### Twitch authorization

To be able to use twitch authorization you need to add
app to dev.twitch.tv and obtain its `client_id` and `secret_id`.
You need to put these into the database along with corresponding SITE_ID.
Check `django-all-auth` documentation for more info.


### Custom commands

1. Import pieces from streamersonglist

* adjust settings to use your `authorization_token`, `streamer_id` and
`attributes_ids`
* run `$ python manage.py import_pieces --api true`

2. Write pieces to nice txt (use case: it can be pasted into google doc)

* adjust settings to use your `authorization_token`, `streamer_id` and
`attributes_ids`
* run `$ python manage.py pieces_to_txt`


## TODO

1. add an actual bot (WIP)
2. fix todo's left in the code
3. regular user shouldn't be able to prioritise queue
4. possibility to set mod permission to user
5. fix all-auth templates to use bootstrap4