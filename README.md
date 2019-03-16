This is the official website of [**t-ui**](https://play.google.com/store/apps/details?id=ohi.andre.consolelauncher) (Linux CLI Launcher). You can access [here](https://whispering-depths-58956.herokuapp.com/).

## Features
+ create a new theme using an easy and lightweight tool
+ upload the theme, or download it as a ZIP file
+ find your favourite theme within a huge list provided by other users
+ you can sort the list by
    * Date
    * Downloads
    * Theme name
    * Author name

<p float="left">
  <img src="http://oi67.tinypic.com/2va1b9h.jpg" width="400" />
  <img src="http://oi64.tinypic.com/1zdvoxs.jpg" width="400" /> 
</p>

## Roadmap
I'll add some features soon. This is the first stable release. Some planned features are:
+ upload a theme from t-ui
+ download a published theme as ZIP
+ edit a published theme (and download/publish it)
+ search a theme by name

## Disclaimer
There are some drawbacks coming with the new website. I'm using Heroku free plan, and so:
+ I get 1000 free dynos for one month (not a big deal)
+ My web-app goes to sleep when no one uses it for 30 minutes (not a big deal, again)
+ My app **has** to sleep at least 6 hourse per day (this **is** a big deal)

I know that it sucks, but I can't afford a paid Heroku plan unfortunately.

## Credits
I'd like to thank some people, which managed the website for a long time for free.
+ Tarun Shanker Pandey
+ Alexander King

When I took the website code, it was HTML+Javascript+PHP. I wanted to try [Django](https://www.djangoproject.com/), so I removed some PHP and Javascript and replaced it with Python (mostly for the server-side operations).

## Open source software
+ Django
+ Gunicorn
+ Postgres
+ dj-database-url
+ WhiteNoise
+ jQuery
+ jscolor
+ JSZip
