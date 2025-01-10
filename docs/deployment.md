# Deployment

We currently deploy on [Toolforge](https://toolsadmin.wikimedia.org/). Please refer to the [Wikitech Help:Toolforge](https://wikitech.wikimedia.org/wiki/Help:Toolforge) documentation.

## Procfile

Toolforge executes commands in the [Procfile](../Procfile) to deploy.

Our Procfile is currently set up to first update the production database using Alembic, then deploy the webservice if that is successful.

## Using Toolforge

### Login

To log into Toolforge and switch to the tool account:

```bash
$ ssh -i /path/to/id_rsa shell-user@login.toolforge.org
$ become wikibase-metadata
```

### Build

To build the tool:

```bash
$ toolforge build start https://github.com/wmde/wikibase-metadata.git
```

You can access a list of builds with `toolforge build list`; please delete old builds using `toolforge build delete build-id`

### Environment Variables

Make sure you have environment variables correct: `toolforge envvars list` should include `SETTINGS_FILE` pointing to the correct `settings.ini` file. To create or update an environment variable, use

```bash
$ toolforge envvars create SETTINGS_FILE prod-settings.ini
```

### Start, Stop, Restart

After building, start the webservice with:

```bash
$ webservice buildservice start --mount=all
```

`stop` and `restart` commands are also available.

### Logs & Shell

For the tail end of the webservice logs, run:

```bash
$ webservice logs
```

To access the active container, run:

```bash
$ webservice shell
```
