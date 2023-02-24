# GamePass Library


## TODO:

### Data

- [x] parse data from google [spreadsheet](https://docs.google.com/spreadsheets/d/1kspw-4paT-eE5-mrCrc4R9tg70lH2ZTFrJOUmOtOytg/edit#gid=0) using [pygsheets](https://github.com/nithinmurali/pygsheets).
- [ ] load parsed data into db.
  - [x] parse genres.
  - [x] parse systems.
  - [x] parse esrbs.
  - [ ] parse games.
- [ ] api:
  - [x] genres.
  - [x] systems.
  - [x] esrbs.
  - [ ] games.
- [ ] fix postgresql docker container.
- [ ] entrypoint for postgres container: setup database and run migrations.

### CI/CD

- [ ] gitworkflows
- [ ] linters
- [ ] git hooks

### Deploy

- [ ] add nginx container.
- [ ] deploy application to digital ocean.
