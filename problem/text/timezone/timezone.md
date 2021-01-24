
# on timezones

Copyright 2021 by John Hanley

Time _should_ be a simple concept to model in a machine,
but apparently there are several pitfalls.
To avoid seeing folks trip over them time and time again,
here are a few hints about timekeeping.

# the nature of time

Time flows.
In exactly one direction.
At a constant rate.

(With apologies to H.G.Wells, and to Einstein --
we consider only ordinary earth-bound observers.)

# timekeeping

We'll skip over
[clepsydræ](https://en.wikipedia.org/wiki/Water_clock#Greco-Roman_world)
to focus on manually wound watches
and Internet-connected digital displays.

![a Mickey Mouse watch](https://upload.wikimedia.org/wikipedia/en/1/1f/Mickey_Mouse_Ingersoll_watch_1933.jpg)

Mickey's hands in the hostage position correspond to 12-noon.

Often our time troubles relate to predicting where Mickey's hands would point.

## TAI

Temps Atomique International is our best available measure
of the passage of time on the Earth's surface.
Among other things it powers GPS time,
with a 19-second offset.

## UTC

Temps universel coordonné is
[TAI](https://en.wikipedia.org/wiki/International_Atomic_Time)
plus leap seconds, occasionally inserted by
[IERS](https://en.wikipedia.org/wiki/International_Earth_Rotation_and_Reference_Systems_Service)
as Earth's rotation slows down.
The value of the UTC time standard always matches
current time within the GMT timezone.
Calibrate your sundial against UTC,
if you don't want to wait for the next equinox.

Wait for a caesium-133 atom to oscillate 9,192,631,770 times.
Finished already? Good, that's 1 second!

## NTP
The [Network Time Protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol)
is how your laptop or linux machine became closely synced with
[UTC](https://en.wikipedia.org/wiki/Coordinated_Universal_Time).

## zone offset

Lunch time in Phoenix is typically noon.
Relative to UTC that is 12:00-0700, a zone offset of seven hours westward,
or 420 minutes.

A particular lunch timestamp might be 2020-10-31 12:00-0700.

Def: a zone offset is a number (like -420) attached to a timestamp.

## timezone

Lunch time in Denver is typically noon MT.
Relative to UTC, in recent years that might be either

- 12:00-0700 MST from November through March, or
- 12:00-0600 MDT from March through November.

In the 1960's, or even in 2005, it would be either

- 12:00-0700 MST from October through April, or
- 12:00-0600 MDT from April through October

since we start observing
[Daylight Saving Time](https://en.wikipedia.org/wiki/Daylight_saving_time_in_the_United_States#1966%E2%80%931972:_Federal_standard_established)
according to the current whim of Congress.
Future whims are fundamentally not predictable.

In the past many changes have been enacted, including
the Federal Fire Prevention and Control Act of 1986 and
the Energy Policy Act of 2005.

States do not _always_ delegate timezone details to Congress.
Eleven entries in the TZ database document the
[illustrious history](https://en.wikipedia.org/wiki/Time_in_Indiana#1960s)
of how Indiana farmers have chosen to synchronize milking time
with interstate commerce.

Note that so-called "standard" time is now observed for only one-third of the year.

Def: a timezone names a **rule** for mapping timestamp to zone offset
in a particular jurisdiction.

Example: America/Denver, which is quite different from America/Phoenix.

As a counter-example, MDT (Mountain Daylight Time) is _not_ a timezone.
Rather, it is a zone offset.
It is essentially the same thing to append MDT or -0600 to a timestamp.

Knowing the Y-M-D is essential to predicting the proper offset,
since the start of DST varies unpredictably over the years.

## U.S. timezones

In the contiguous 48, five zones are currently used. Their rule names are:

- America/Los_Angeles, -8 modulo Daylight Saving
- America/Denver, -7 modulo Daylight Saving
- America/Phoenix, -7 always
- America/Chicago, -6 modulo Daylight Saving
- America/New_York, -5 modulo Daylight Saving

# computing

## serialized form

When storing a timestamp,
_always_ write the UTC form to persistent storage.

Upon retrieving it from disk,
we can _then_ apply a zone offset
so that numeric output will match position of Mickey's hands
for the user viewing the result.
Note that we will need to know the user's favorite timezone
in order to show the expected result.
Consider making the applied offset **explicit** in the output,
e.g. by appending "ET", "EST", or "EDT".

When serializing in text (.csv) or JSON form,
consider appending "Z" or, better, "-0000".
Then it will be clear to anyone reading it that these are UTC stamps.

## python datetime

The standard library has the curious notion of naïve and aware instances.
Using the default, naïve, works tolerably well.

For any _new_ development effort,
consider using stamps that look like this:

    import datetime as dt

    ts = dt.datetime(2020, 10, 31).replace(tzinfo=dt.timezone.utc)

This makes things nicely explicit.

Note that you will probably want all timestamps in your codebase
to follow this practice, since naïve and aware are not comparable.
You cannot e.g. mix them in `stamps` and then use `sorted(stamps)`.

## pytz

For timezone conversions, you will certainly want
[`import pytz`](https://pythonhosted.org/pytz).

Prefer the five "America/" timezone names mentioned above.

## uszipcode

Given a ZIP code, it is easy to learn which TZ jurisdiction it is in.

Use [`import uszipcode`](https://pypi.org/project/uszipcode)
and query the `timezone` field to obtain the local TZ rule name.
Then feed that to `pytz`.
