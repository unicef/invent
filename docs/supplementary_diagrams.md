# Supplementary Diagrams

## Physical Data Model (PDM)
The DB PDM is presented in the following image:
:::{figure-md} db-pdm-diagram

<img src="./_static/images/pdm/database.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**DB PDM**
:::

The following sections zoome into the PDM of each Django application.

### Core
:::{figure-md} core-pdm-diagram

<img src="./_static/images/pdm/core_database.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**DB PDM**
:::

### Country
:::{figure-md} country-pdm-diagram

<img src="./_static/images/pdm/country_database.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**DB PDM**
:::

### Project
:::{figure-md} project-pdm-diagram

<img src="./_static/images/pdm/project_database.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**DB PDM**
:::

### Search
:::{figure-md} search-pdm-diagram

<img src="./_static/images/pdm/search_database.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**DB PDM**
:::

### User
:::{figure-md} user-pdm-diagram

<img src="./_static/images/pdm/user_database.png" alt="system-context-diagram" class="bg-primary mb-1" width="600px">

**DB PDM**
:::


### Note: How to export database schema
Pygraphviz is a Python interface to the Graphviz graph layout and visualization package and is required to draw graphs of the physical data model. This can be added under ```django/requirements.txt``` and be installed while executing docker-compose build.
```bash
cd <GIT_REPOSITORY_NAME>/django
```

Add the following line in requirements.txt file
```
pygraphviz==1.7
```

Then execute:
```bash
cd <GIT_REPOSITORY_NAME>
docker-compose build
docker-compose up
```

Pygraphviz needs graphviz software to run. In the terminal execute the following to find the tiip-django container id.
```bash
docker ps -a
```

Then use the following command to start an interactive shell inside django docker container. This will run the bash shell in the specified container, giving a basic shell prompt. To exit back out of the container, type ‘exit’ and then press ENTER:
```bash
docker exec -it <CONTAINER_ID> bash
```

While in the container install the software by executing:
```bash
apt-get install graphviz
```

Open a new terminal and run 
```
docker-compose exec django python manage.py graph_models app -o image_filename.png
```

Where:
* ```app```: the django application to export the DB schema, eg user or project etc
* ```image_filename.png```: a filename to store the output png file of database

To get the schema of more than one application and the relationship between them execute the following: 
```bash
docker-compose exec django python manage.py graph_models app1 app2 app3 -o image_filename.png
```



