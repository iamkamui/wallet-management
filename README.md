<a id="readme-top"></a>


<!-- PROJECT SHIELDS -->
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

<h2 align="center">Wallet Management Challenge</h2>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is a wallet management forked from a [challenge](https://github.com/WL-Consultings/challenges). I used this project to improve my knowledge and learn new approach of development.
To achieve all requirements of challenge, i used [DjangoStyleGuide](https://github.com/HackSoftware/Django-Styleguide) repo, documentation of Djando Rest Framework and Django as base to guide my development.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Python][Python.py]][Python-url] [![DRF][Django REST framework]][DRF-url] [![Django][Django]][Django-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

For this project i'm using ["uv"](https://docs.astral.sh/uv/) for package management, the choice to behind using this package management is for test the performance, complexity and avoid compatibility issues.

Feel free for use any package management that is better for you, but for the guide i'll perform with uv.


### Prerequisites

This project uses uv for package management, ad was built in docker environment, make sure that have all prerequisites installed before continue


- [uv](https://docs.astral.sh/uv/getting-started/installation/) >= 0.7.5
- [Docker](https://docs.docker.com/compose/install/) >= 28.1.1
- [Docker compose](https://docs.docker.com/engine/install/) >= 2.35.1

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/iamkamui/wallet-management.git
   ```

2. Install dependencies
> If you are using uv the virtual environment will be created automaticaly

   ```sh
   uv sync --lock
   ```

3. Copy and fill in your environment viables
   ```sh
   $ cp example.env .env
   ```

4. Build and run the containers
   ```sh
   docker compose up -d
   ```

5. Activate virtual environment and run the tests
  * Linux
   ```sh
   source .venv/bin/activate && make test_all
   ```

6. Run migrations and populate with preload data
> Take a look at `backend/wallet_management/fixtures/base_data.json` to understand what data will be loaded
   ```sh
   make initial_migrate
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

For initial usage the project has two users with fake data created to test propose. The project use JWT as authentication method, to receive your access token send a post request to `/api/auth/token/` endpoint with user data payload below on request body.


* User 1
```json
{
   "cpf": "29615434876",
   "password": "passwd@seguro"
}
```

* User 2
```json
{
   "cpf": "29107448686",
   "password": "passwd@seguro"
}
```

* Example
```sh
curl -X POST \
  http://0.0.0.0:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"cpf": "29615434876", "password": "passwd@seguro"}'
``` 

If for some reason you need a admin user just perform `make superuser`

> To obtain a list of available endpoints just follow http://0.0.0.0:8000/api/schema/redoc/
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Pedro Augusto - [Linkedin](https://www.linkedin.com/in/pedro-augusto-b445b019b/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/pedro-augusto-b445b019b/

[Django REST framework]: https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray
[DRF-url]: https://www.django-rest-framework.org/

[Python.py]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white&color=4FC08D&labelColor=gray
[Python-url]: https://www.python.org/

[Django]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white&labelColor=gray
[Django-url]: https://www.djangoproject.com/