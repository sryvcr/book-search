# Library Administration

## Run Webapp
1. Clone the Library Administration repository
2. Move to develop branch:  
```bash
$ git checkout develop
```
3. To run webapp execute in console (make sure you are on the root project directory):  
```bash
$ make run
```

4. To stop web app execute:
```bash
$ make down
```

### The following commands need to have webapp container running
To make django migrations execute:  
```bash
$ make mkmigration
```

To make apply django migrations to db execute:  
```bash
$ make migrate
```

To enter into django shell execute:  
```bash
$ make dj-shell
```

To run tests execute:  
```bash
$ make test
```