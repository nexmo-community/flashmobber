# Nexmo Flashmobber

This is a demo project under heavy development.

## Installing It:

You'll need Python 3.6 (f-strings!) and [Pipenv] installed. Run the following to set up your environment:

```shell
pipenv install
pipenv shell
```

## Running It:

To run it you'll need to set the following environment variables. This can be done either by editing the values in the `config.env` file and sourcing it using `source config.env` or using Foreman or Envdir.

```
# Nexmo credentials:
declare -x NEXMO_API_KEY=your-nexmo-api-key
declare -x NEXMO_API_SECRET=your-nexmo-api-secret
declare -x NEXMO_PRIVATE_KEY=your-nexmo-private-key
declare -x NEXMO_APPLICATION_ID=your-nexmo-application-id
declare -x NEXMO_SIGNATURE_SECRET=your-signature-secret (Contact Nexmo Support)
declare -x NEXMO_SIGNATURE_METHOD=your-signature-encryption-method (Contact Nexmo Support)

# Some Django config:
declare -x SECRET_KEY=a-random-string
declare -x DEBUG=true
declare -x ALLOWED_HOSTS=comma-separated-domain-list

# Pusher app credentials:
declare -x PUSHER_APP_ID=id
declare -x PUSHER_APP_KEY=key
declare -x PUSHER_APP_SECRET=secret
declare -x PUSHER_APP_CLUSTER=cluster-country-code
```

You'll also need to configure Nexmo to send you SMS using JSON and POST!

Then run:

```shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

[pipenv]: https://docs.pipenv.org/

## To Do

* Revamp the interface for purchasing numbers (currently the interface for buying numbers isn't even linked in.)
* Add interface to send a message to registered participants
* General appearance improvements
* Style the event billboard page!

## Ideas

* Contact QR code on the billboard to make sending SMS easier!
