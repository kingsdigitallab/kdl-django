# Django LDAP authentication

This application uses [django-auth-ldap][] to authenticate against DDH's LDAP
service. If the LDAP authentication fails it falls back to Django
authentication, so it is possible to have local Django accounts.

## Configuration

- Add ddhldap_django to your project
- Install the [requirements][]
- Import the ddhldap_django settings into your project:
`from ddhldap_django.settings import *`.
- Add the setting `AUTH_LDAP_REQUIRE_GROUP` to your project settings and set
it to the LDAP group you want to authenticate to. For example for the *histpag*
group you would need to do:
`AUTH_LDAP_REQUIRE_GROUP = 'cn=histpag,' + LDAP_BASE_OU`.
- Add ddhldap_django signal handler into your project urls:
    
        from ddhldap.signal_handlers import register_signal_handlers as \
            ddhldap_register_signal_hadlers
        ddhldap_register_signal_handlers()

## System requirements

The python/django LDAP libraries depend on the libldap2-dev and libsasl2-dev system
libraries.

[django-auth-ldap]: http://pythonhosted.org/django-auth-ldap/
[requirements]: requirements.txt
