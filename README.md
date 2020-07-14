<h1>pynote_api</h1>
pynote_api is a backend service for working with notes.
Supports JWT authorization and caching.
<hr>
<a href="https://www.notion.so/mikhailkhmel/9513e80fa21248a798c8db4be443ccb7?v=f7066966ff9442588ec5b0726b65b034">API</a>
<hr>
<h2>Installation</h2><br>
<code>python -m venv venv</code><br>
For Windows: <code>venv\Scripts\activate</code><br>
For Linux/MacOS: <code>source venv/bin/activate</code><br>
<code>pip install -r requirements.txt</code><br>
Configure the config.py file as you need<br>
Set a environment variable<br>
For Windows: <code>set APP_SETTINGS=config.{Class From config.py}</code><br>
For Linux/MacOS: <code>export APP_SETTINGS=config.{Class From config.py}</code><br>
Make Migrations for Database <br>
<code>
python manage.py db init <br>
python manage.py db migrate <br>
python manage.py db upgrade <br>
</code>
Run app <br>
<code>python app.py</code>