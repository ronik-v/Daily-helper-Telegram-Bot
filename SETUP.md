# Base setup for project
<div class="wrapper">
    <ul class="task-list">
        <li>
            <h3>Create database in postgresql with name DailyHelper</h3>
            <pre>postgres=# CREATE DATABASE DailyHelper;<br>postgres=# \c dailyhelper;<br>postgres=# \i 'way_to_project/database/rates_and_news.sql';</pre>
        </li>
        <li>
            <h3>Run parsers that will add all the information to (Rates/FinNews)</h3>
            <pre>python3 .\database_update.py</pre>
        </li>
        <li>
            <h3>Add all data your database to the config file</h3>
            <pre>db_config: dict[str, str] = {
	'db_name': 'dailyhelper',
	'user': 'USER',
	'password': 'PASSWORD',
	'host': 'localhost'
}           </pre>
        </li>
    </ul>
</div>