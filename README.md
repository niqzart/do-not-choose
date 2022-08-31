# And Don't Choose
*Inspired by local memes*

## Description
This is a learning project made to better understand python web frameworks and complex server setups. There will be multiple implementations of the [basic interface](#waves), with using different [database systems](#databases), as well different [framework](#frameworks) (python or maybe other in the future). These implementations will be united using a complex [server setup](#server-setup).

## Waves
Each implementation will be done in waves and tagged along the way for easier navigation. Each wave requires implementing a part of the [basic interface](SPEC.md). *A wave will be described in full after any full (database + framework) implementation reaches the previous wave*

### W1 (Base)
- Basic Configuration
- Simplest Endpoint(s)
- X-Framework header for all requests
- Error handlers (404, 500)

### W2 (Reglog)
- User & block-list data structures
- Classic authorization services
- Blocking user tokens for sign-out
- One protected resource (`/home/`)

### W3 (CRUDLs)
- Games & Participant tables (+cascades)
- Pagination with filters & sorts
- Participant listing for participants
- Updating & deleting for owners only

### W4 (Going Duplex)
TBD

## Databases
### Relational (via SQLAlchemy) [A]
*Codename A, because alchemy sounds fun*

### MongoDB (via MongoEngine) [M]
*Codename M, the letter after N, as in noSQL*

### Redis (via RedisPy) [E]
*Codename E, because...*

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

| codename |       wave1       |       wave2       | wave3 | wave4 | 
|:--------:|:-----------------:|:-----------------:|:-----:|:-----:|
|    A     | w1a [26 Aug 2022] | w2a [30 Aug 2022] |       |       |
|    M     |                   |                   |       |       |
|    E     |                   |                   |       |       |
|    F     | w1f [30 Aug 2022] | w2f [30 Aug 2020] |       |       |
|    R     |                   |                   |       |       |
|    X     | w1x [25 Aug 2022] |                   |       |       |
|    B     | w1b [31 Aug 2022] |                   |       |       |
|    P     |                   |                   |       |       |

## Server Setup
TBA
