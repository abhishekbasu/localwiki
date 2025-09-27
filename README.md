# localwiki

Your own personal wiki to run locally when you don't have access to the internet. This is very much a work in progress, and is primarily to serve my needs. Mostly built during one coding session while catching up on news - so please be patient :)

## Instructions

If you're on macOS, first install Homebrew on your system. Then use the Makefile to install dependencies and take it for a spin!

```bash
make install
make first-run
```

These commands will install dependencies, set up the database. This takes a few minutes, but thankfully you only need to do it once.

Now to start a local server run,

```bash
make serve
```

And you can go to `http://localhost:8000` in your browser to see your local wiki.

![screenshot](public/localwiki.png)

## Troubleshooting

To remove the sqlite db, run

```bash
make clean
```
