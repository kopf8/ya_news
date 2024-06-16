# YaNews
### YaNews is a website with newsfeed, where users can leave their comments on every news' page.

## Project description

* The main page of the project displays 10 latest news in descending order (last to first).
Main page is accessible for any user. Every news is displayed in a truncated form (only the first 15 words are visible).
* Each news has its own page, with the full text of the news; user comments are also displayed there.
* Any user can register on the site independently.
* Authorized user can leave comments, edit and delete his/her/their comments.
* If there are comments on the news, their number is displayed on the main page in brackets under the news.
* The project code contains a list of prohibited words that cannot be used in comments, for example, "редиска" and "негодяй".

### Project tech stack:

Python, Django, HTML, SQLlite3, pytest, unittest

## Tests for YaNews

### In file test_routes.py:
* Main page, separate news page, login/logout/sign-up pages are all accessible to an anonymous user.
* An authorized user cannot access the pages for editing or deleting other users' comments (error 404 is returned).
* The comment deletion and editing pages are available only to the comment author.
* When trying to load the edit or delete comment page, the anonymous user is redirected to the authorization page.

### In file test_content.py:
* The number of news items on the main page is no more than 10.
* The news is sorted from the most recent to the oldest in descending chronological order (the latest news is displayed at the top of the list).
* Comments on a separate news page are sorted in ascending chronological order: old ones at the beginning of the list, new ones - at the end.
* Anonymous user cannot use the form to leave a comment on a separate news page, but an authorized user can use the form.

### In file test_logic.py_:
* Anonymous user cannot leave a comment.
* Authorized user can leave a comment.
* If a comment contains forbidden words, it will not be published, and the form will return an error.
* Authorized user can edit or delete his/her/their comments.
* Authorized user cannot edit or delete other people's comments.
* Unauthorized user cannot edit or delete any comments.

### How to run the project:

Clone repository and switch to project directory using command line:

```
git@github.com:kopf8/ya_news.git
```

```
cd ya_news
```

Create & activate virtual environment:

```
python -m venv env
```

* For Linux/macOS:

    ```
    source env/bin/activate
    ```

* For Win:

    ```
    source env/Scripts/activate
    ```

Upgrade pip:

```
python -m pip install --upgrade pip
```

Create .env file and fill it as per example:

```
SECRET_KEY = <your-secret-key>
```

Install project requirements from file _requirements.txt_:

```
pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Load fixtures:

```
python manage.py loaddata news.json
```

Run project:

```
python manage.py runserver
```

Run project tests:
* Pytest:

    ```
    pytest
    ```

* Unittest:

    ```
    python manage.py test news.tests
    ```

### Author:
**Maria Kirsanova**<br>
Github profile — https://github.com/kopf8