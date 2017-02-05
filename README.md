# Pipeline [<img align="right" width="200px" src="https://cloud.githubusercontent.com/assets/335234/18211402/6fb5bdd6-710b-11e6-93dc-f47559d8ba19.png">](https://poly.rpi.edu)

Pipeline is a tool for content organization, tracking, and distribution. _The Rensselaer Polytechnic_ is spearheading its development for its own use, but it is generic enough that it can be used by other media organizations looking for an open-source newsroom management suite.

## Goals

### Organization

Pipeline tracks stories from start to finish. As soon as an idea is proposed, it can be entered into Pipeline by an editor. Reporters and photographers can be assigned, and details about the story—such as event location and time, people to contact, and related tasks—can be recorded.

### Tracking

As a story is written, goes through the copyreading process, and is eventually published, a history of edits is recorded. Copy readers can easily see where stories are in the copy queue and advance them as they are edited.

### Distributing

After a story has been copy read, it can be pushed into Adobe InDesign for layout and published on a website. The website will be mostly decoupled and get its content from the stable Pipeline API, allowing for website development to occur without strict coordination with the Pipeline maintainers.

## Motivation

Currently, by the time a story is published, it exists in three separate places: Google Drive, InDesign layout files, and https://poly.rpi.edu. There is no single, authoritative history of edits. Additionally, the organization of each issue's content is currently done within a spreadsheet, and it is not associated with the resulting articles. Our goal is to reduce overhead and streamline the story creation, editing, and publishing process.

## Running Pipeline

Pipeline's API is written in Python, and it uses Angular and TypeScript on the
frontend. To run it for development, install [Docker](https://www.docker.com/products/overview), clone this repo, run `docker-compose up`, and then check out [localhost:8000](http://localhost:8000). Take a look at the Dockerfiles in the API, web, and rt-editor folders to figure out how the containers are built.

Docker Hub builds three containers from this repo, and they can be found on [_The Poly_'s Hub page](https://hub.docker.com/u/thepoly/).
