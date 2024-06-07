# Tweet-ANalytics-TOol (TANTO)

This code contains all the source code to build and use the platform developed during the project [StandByMe 2.0](https://www.standbymeproject.eu/stand-by-me-2-0/) (Top gender-bAsed violeNce by aDdressing masculinities and changing Behaviour of Young people through huMan rights Education, CERV-2021-DAPHNE, proposal n. 101049386).

This repository is divided into two parts: the API (written in Python) and the UI (written in VueJS).

## Python backend (API)

The `api` folder contains the files neede to run the Python backend.
To execute it, first one has to install the requirements by running `pip install -r api/requirements.txt`.

After that, a folder called `data` must be created, containing `datasets.json`, a configuration file where the datasets are listed and described.

This is an example:

```
{
	"dataset_name_1.csv": {
        "lang": "it",
        "date_start": "2012-01-01",
        "date_end": "2022-01-01",
        "description": "Dataset description",
        "name": "Dataset name"
    },

    ...
}
```

For each dataset in the configuration file, a CSV file with the same name should be created in the `data` folder. In the example, a file named `dataset_name_1.csv` should be created.

The file should contains the tweets data. The first row would contain the column names. For instance:

```
,timestamp_utc,lang,id,retweeted_id,quoted_id,to_userid,hashtags,text,textLemm
0,1650717064,it,15178736945792772,,,,,Tweet text,Tweet text lemmatized
...
```

Finally, to run the backend just run (from the `api` folder) the following command:

```
uvicorn server:app --host 0.0.0.0 --port 9101 --reload
```

Parameters for `--host` and `--port` can be modified as preferred. The `--reload` argument is used to reload the program when any Python file is modified.

## User interface

The user interface is included in the `ui` folder and needs Node to be executed.
To run it in serve mode, just run `npm run serve`.

There are two environment variables that should be set: `BASE_URL` and `BASE_API`.

* `BASE_URL` is the URL where the web interface is to be installed (for instance `/sbm2-ui/` if the final address would be `https://example.com/sbm2-ui/`);
* `BASE_API` is the link to the API (for instance, `https://example.com/sbm2-api`).

To build the final distribution package, run:

```
BASE_URL=/sbm2-ui/ BASE_API=https://example.com/sbm2-api npm run build
```

## Project info

Grant info: 101049386 — STANDBYME 2.0 — CERV-2021-DAPHNE – Funding: Funded by the Citizens, Equality, Rights and Values Programme (CERV-2021-DAPHNE)
