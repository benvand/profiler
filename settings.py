

class Constants(object):
    FILE = 2
    STDOUT = 4




METRICS = { # analyse default
    'default': { # host:port/url
        'url': 'adwords',
        'host': 'google.com',
        'port': 80,
        'timeout': 10, # Considered a failure. Drops attempt
        'tries': 10, # amount of times this connection should be tried. stats will be an average
        'report_type': Constants.STDOUT
    },
}






