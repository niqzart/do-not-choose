# And Don't Choose
*Inspired by local memes*

## Description
This is a learning project made to better understand python web frameworks and complex server setups. There will be multiple implementations of the same [basic interface](#waves), each using a separate [framework](#frameworks) (python or maybe other in the future). These implementations will be united using a complex [server setup](#server-setup).

## Waves
Each implementation will be done in waves and tagged along the way for easier navigation. Each wave requires
implementing a part of the [basic interface](SPEC.md). *Wave will be described in full after any implementation reaches
the previous wave*

### W1 (Base)
- Basic Configuration
- Simplest Endpoint(s)
- X-Framework header for all requests
- Error handlers (404, 500)

### W2 (Reglog)

- Attach the common SQLAlchemy DB
- Classic authorization services
- One protected resource (`/home/`)
- User session management

### W3 (CRUDLs)

- Main bulk of the ReST endpoints
- Simplest file upload-download system
- Protected non-safe methods

### W4 (Going Duplex)

- Duplex setup and configuration
- Rooms & broadcasting events
- Integration with ReST

## Databases

!NEW!

## Frameworks

### Flask [F]

*Codename F, the sixth letter from micro-Framework*

### Flask + Flask-RESTX [R]

*Codename R, the sixth letter from the library name*

### Flask + Flask-Fullstack [X]

*Codename X, in honour of [xi.effect](https://github.com/xieffect)*

### Falcon [B]
*Codename B, because [falcon](https://en.wikipedia.org/wiki/Falcon) is a Bird...*

### FastAPI [P]
*Codename P, because performance, I guess*

### Might be added
- Tornado
- Pyramid
- Dash
- Django RF
- Node.js

## Progress
*Tags and dates per implementation per wave*

| codename |       wave1       | wave2 | wave3 | wave4 | 
|:--------:|:-----------------:|:-----:|:-----:|:-----:|
|    F     | w1f [30 Aug 2022] |       |       |       |
|    R     |                   |       |       |       |
|    X     | w1x [25 Aug 2022] |       |       |       |
|    B     |                   |       |       |       |
|    P     |                   |       |       |       |

## Server Setup
TBA
