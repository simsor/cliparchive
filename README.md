# cliparchive

## Description

A set of scripts to download games from the [Wayback Machine](https://web.archive.org)'s archive of Miniclip.com, and a Web frontend to play them using [ruffle](https://ruffle.rs/).

The embedded Ruffle comes from [my fork](https://github.com/simsor/ruffle) (way behind upstream now), which adds the ability to redirect external HTTP requests from the SWF file to your own data, for preservation purposes. This project doesn't use this feature yet, but it can come in handy!

## Known bugs

- Some games have an anti-piracy measure, which prevents them from working.
- Some games don't work very well with Ruffle. I'll have to update my fork.

## Try it out

https://simsor.github.io/cliparchive/