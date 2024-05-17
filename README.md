<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/6295/6295417.png" width="100" />
</p>
<p align="center">
    <h1 align="center">INFRAMAPDATABASE</h1>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/FNS-Division/inframapdatabase?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/FNS-Division/inframapdatabase?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/FNS-Division/inframapdatabase?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/FNS-Division/inframapdatabase?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=flat&logo=GNU-Bash&logoColor=white" alt="GNU%20Bash">
	<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=flat&logo=YAML&logoColor=white" alt="YAML">
	<img src="https://img.shields.io/badge/MySQL-4479A1.svg?style=flat&logo=MySQL&logoColor=white" alt="MySQL">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white" alt="pandas">
	<img src="https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white" alt="NumPy">
</p>
<hr>

##  Overview

This project provides a suite of Python scripts and configuration files for managing a database of telecommunication infrastructure information. It allows you to create and interact with a MySQL database schema designed to store data on Point of Interest (POI) locations, cell sites, transmission nodes, costs and mobile coverage.

The included scripts handle:

- Database creation
- Data loading
- Data manipulation
- Data retrieval

In order to create a local database on a Ubuntu machine, follow the commands in script `create_local_mysql_db.sh`. The provided codes allow for interacting with either a local databse, or a database hosted on Amazon Web Services (AWS).

---

##  Repository Structure

```sh
└── inframapdatabase/
    ├── 00_create_data_model.py
    ├── 01_add_data.py
    ├── 02_delete_data.py
    ├── 03_query_data.py
    ├── LICENSE
    ├── README.md
    ├── create_local_mysql_db.sh
    ├── credentials
    │   ├── aws_db_credentials.py
    │   └── local_db_credentials.py
    ├── data
    │   └── ESP
    │       ├── costinputs
    │       │   └── esp_costs_test.xlsx
    │       ├── output
    │       │   ├── cost
    │       │   │   ├── ESP-1714391188-zq9z-cost-results-poi-info.csv
    │       │   │   └── ESP-1714391188-zq9z-cost-results.csv
    │       │   ├── fiberpath
    │       │   │   ├── ESP-1715934412-1pka-edges.csv.csv
    │       │   │   ├── ESP-1715934412-1pka-nodes.csv.csv
    │       │   │   └── ESP-1715934412-1pka-results.csv.csv
    │       │   ├── pcd
    │       │   │   └── ESP-1708346219-hhao-pcd.csv
    │       │   └── visibility
    │       │       └── ESP-1708423221-tgah-visibility.csv
    │       ├── population
    │       │   └── esp_ppp_2020_1km_Aggregated_UNadj.tif
    │       ├── processed
    │       │   ├── cellsite
    │       │   │   └── ESP-1697916284-6wv8-cellsite.csv
    │       │   ├── mobilecoverage
    │       │   │   └── mobile_coverage_merged_fixed_geom.gpkg
    │       │   ├── pointofinterest
    │       │   │   └── ESP-1697915895-xs2u-pointofinterest.csv
    │       │   └── transmissionnode
    │       │       └── ESP-1697916384-1icf-transmissionnode.csv
    │       └── srtm1
    │           └── readme.txt
    ├── datamodel.py
    └── environment.yml
```

---

##  Modules

<details closed><summary>database operations</summary>

| File                                                                                                              | Summary                                              |
| ---                                                                                                               | ---                                                  |
| [00_create_data_model.py](https://github.com/FNS-Division/inframapdatabase/blob/master/00_create_data_model.py)   | `00_create_data_model.py`  |
| [01_add_data.py](https://github.com/FNS-Division/inframapdatabase/blob/master/01_add_data.py)                     | `01_add_data.py`           |
| [02_delete_data.py](https://github.com/FNS-Division/inframapdatabase/blob/master/02_delete_data.py)               | `02_delete_data.py`        |
| [03_query_data.py](https://github.com/FNS-Division/inframapdatabase/blob/master/03_query_data.py)                 | `03_query_data.py`         |
| [datamodel.py](https://github.com/FNS-Division/inframapdatabase/blob/master/datamodel.py)                         | `datamodel.py`             |
| [create_local_mysql_db.sh](https://github.com/FNS-Division/inframapdatabase/blob/master/create_local_mysql_db.sh) | `create_local_mysql_db.sh` |
| [environment.yml](https://github.com/FNS-Division/inframapdatabase/blob/master/environment.yml)                   | `environment.yml`          |

</details>

<details closed><summary>credentials</summary>

| File                                                                                                                        | Summary                                                         |
| ---                                                                                                                         | ---                                                             |
| [local_db_credentials.py](https://github.com/FNS-Division/inframapdatabase/blob/master/credentials/local_db_credentials.py) | `credentials/local_db_credentials.py` |
| [aws_db_credentials.py](https://github.com/FNS-Division/inframapdatabase/blob/master/credentials/aws_db_credentials.py)     | `credentials/aws_db_credentials.py`   |

</details>

---

##  Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `version 3.9`

###  Installation

1. Clone the inframapdatabase repository:

```sh
git clone https://github.com/FNS-Division/inframapdatabase
```

2. Change to the project directory:

```sh
cd inframapdatabase
```

3. Install the dependencies:

```sh
conda env create --file environment.yml
conda activate dbsetupenv
```

###  Running inframapdatabase

Use the following command to run inframapdatabase:

```sh
python3 00_create_data_model.py
python3 01_add_data.py
...
```

---
