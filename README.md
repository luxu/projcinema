# projcinema

## Acessando o projeto

To download the project to your machine:
> `git clone https://github.com/luxu/projcinema.git`

OR

You can download the zipped file and then unzip:
> `https://github.com/luxu/projcinema/archive/master.zip`

To isolate the libraries used in this project from the others of their use create a virtual environment.

> No Windows: pip install virtualenv

> No Linux: pip3 install virtualenv

After that, go to the project folder:
> cd projcinema

E crie o ambiente virtual:

> virtualenv venv

Para ativar o virtualenv:

> Windows: venv/Scripts/activate

> Linux: source venv/bin/activate


To install the libraries
> Windows: pip install -r requeriments.txt

> Linux: pip3 install -r requeriments.txt

Some Required Libraries:
* `Requests`
* `Beautifoul Soup`
* `csfscrape`

To run the project:
- python main.py

#### Note:
##### `The project was divided into folders to facilitate maintenance`

```
Main file at the root of the project: "main.py"
```

To rotate the scripts: `Python 3.6+`

##### The file cathay.py generates a file cathay.json that is all the movies of the site, after this is made the reading of the JSON and it gets only the some data as it is printed on the screen
