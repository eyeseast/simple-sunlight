Simple Sunlight
===============

Sometimes, all you need is the data. This is the simplest possible wrapper I could make. It returns decoded JSON, with some fat trimmed. It should stay out of your way.

Usage:

    >>> from sunlight import Sunlight
    >>> sunlight = Sunlight(API_KEY)
    >>> pelosi = sunlight.legislators.get(lastname='pelosi')
    >>> print pelosi['firstname']
    Nancy

This should work with any method on Sunlight' Congress API defined here: http://services.sunlightlabs.com/docs/Sunlight_Congress_API/

See test.py for more details and examples.