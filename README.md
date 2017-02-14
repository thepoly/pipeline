# Pipeline

Pipeline is a tool for content organization, tracking, and distribution. [_The
Rensselaer Polytechnic_](https://poly.rpi.edu) is spearheading its development
for its own use, but it is generic enough that it can be used by other media
organizations looking for an open-source newsroom management suite.

## Goals

### Organization

Pipeline tracks stories from start to finish. As soon as an idea is proposed, it
can be entered into Pipeline by an editor. Reporters and photographers can be
assigned, and details about the story—such as event location and time, people to
contact, and related tasks—can be recorded.

### Tracking

As a story is written, goes through the copyreading process, and is eventually
published, a history of edits is recorded. Copy readers can easily see where
stories are in the copy queue and advance them as they are edited.

### Distributing

After a story has been copy read, it can be pushed into Adobe InDesign for
layout and published on a website. The website will be mostly decoupled and get
its content from the stable Pipeline API, allowing for website development to
occur without strict coordination with the Pipeline maintainers.

## Motivation

Currently, by the time a story is published, it exists in three separate places:
Google Drive, InDesign layout files, and https://poly.rpi.edu. There is no
single, authoritative history of edits. Additionally, the organization of each
issue's content is currently done within a spreadsheet, and it is not associated
with the resulting articles. Our goal is to reduce overhead and streamline the
story creation, editing, and publishing process.

## Running Pipeline

Pipeline's API is written in Python, and it uses Angular and TypeScript on the
frontend. To run it for development:

1. Install [Docker](https://www.docker.com/products/overview)
2. Clone this repo
3. Run `docker-compose up`

Pipeline's web interface will be running on
[localhost:8000](http://localhost:8000). The API will be at
[localhost:8001](http://localhost:8001).

Take a look at the Dockerfiles in the API, web, and rt-editor folders to figure
out how the containers are built.

Docker Hub builds three containers from this repo, and they can be found on
[_The Poly_'s Hub page](https://hub.docker.com/u/thepoly/).

### Tests

Pipeline currently has incomplete tests for its API. They require Docker, and
can be run by executing `api/tests/test.sh`.

### Troubleshooting

If you're seeing weirdness, try rebuilding the containers with `docker compose
up --build`. If it persists, please contact a team member or open an issue.
