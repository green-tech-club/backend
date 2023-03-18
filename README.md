# greentech_api

Here is a quick [demo video](https://www.youtube.com/watch?v=dQw4w9WgXcQ) about how it works.

1. clone the repo
2. pip install -r .\requirements.txt
2. create your own `.env` file
3. paste these lines in it:
-   `db_username = "your_userid"`
-   `db_password = "your_pass"`
-   `db_cluster = "cluster0.777"`
4. replace the credentials with yours.
5. `python .\app\main.py`
6. open in your browser: http://127.0.0.1:8000/docs

Under the `.\examples\` folder there are some examples like `delete.html` and `update.html` to show how a request towards the API should look like.
 
 You can serve them with python by:
 - `cd .\examples`
 - `python -m http.server 3333`