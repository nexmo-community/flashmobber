# Nexmo Flashmobber

This is a demo project under heavy development.

## Installing It:

You'll need Python 3.6 (f-strings!) and Pipenv installed. Run the following to set up your environment:

```shell
pipenv install
pipenv shell
```

## Running It:

To run it you'll need to set the following environment variables, either directly, or using Foreman or Envdir:

```
declare -x NEXMO_API_KEY=your-nexmo-api-key
declare -x NEXMO_API_SECRET=your-nexmo-api-secret
declare -x NEXMO_SIGNATURE_SECRET=your-signature-secret (Contact Nexmo Support)
declare -x NEXMO_SIGNATURE_METHOD=your-signature-encryption-method (Contact Nexmo Support)
declare -x SECRET_KEY=a-random-string
declare -x DEBUG=false
declare -x ALLOWED_HOSTS=comma-separated-domain-list
```

Then run:

```shell
python manage.py migrate
python manage.py runserver
```