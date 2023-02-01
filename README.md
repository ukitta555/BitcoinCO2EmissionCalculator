<h1> Bitcoin Emissions CO2 API</h1>
<h2> Disclaimer </h2>
<p> 
    Although the author of this README tried to make this tutorial as
    detailed as possible, please feel free to reach out in case something does
    not work as expected or some commands are missing. Thank you!
</p>
<h2> Python version </h2>
Project was built on top of Python 3.10.
<h2> Assumptions </h2>
<p>
    All commands supplied assume you run LTS version of Ubuntu Linux. 
    You'll also need a PostgreSQL installation to run this API 
    (this topic goes out of the scope of this README, please Google how to install it). 
</p>
<p>
    In case you have Windows/MacOS, commands might differ and the author encourages you to find alternatives and complement this README with MacOS/Windows secitons.
    This README also assumes basic Python,Git and Linux proficiency, and the ability to not get frustrated easily in case something goes wrong ;)
</p>
<h2> Running API locally</h2>
<p>
    First of all, clone the API source code with <code>git clone</code> command.
</p>
<p>
    Then, switch the working directory of the terminal with <code> cd ~type_project_directory_path_here~" </code> command.
</p>
<p> 
    You might want to create a virtual environment for this project to not trash your OS Python installation with additional packages, but it is optional. 
    In case you go for it, make sure that you have the <code>venv</code> package installed before creating a virtual environment (below is the command used to install python <code>venv</code> package for Ubuntu Linux).
</p>
<code> sudo apt-get install python3-venv </code>
<p>
    To create the virtual environment and to activate it (assuming you <code> cd</code>'ed to project's folder):
</p>
<code> python3 -m venv venv && source /venv/bin/activate</code>
<p> To install the dependencies:</p>
<code> pip install -r requirements.txt </code>
<p> 
    You would also need to create an .env file inside <code>/src</code> folder. 
    To find variables that you need to fill in, search the project for <code>os.environ.get</code> calls.
</p>
<p>
    You also need to run the migration to populate the DB with required tables:
    <code> ./manage.py migrate</code>
</p>
<p> Finally, to run the API locally, navigate to the project folder and use the following command in the terminal:</p>
<code> ./manage.py runserver </code>
<p> The API should be running on <code>127.0.0.1:8000</code>.</p>
<h2> I'm able to run the API locally. What are my next steps?</h2>
<p>  </p>
<p> The API only serves the final calculation results to the user - most of the calculations happen "in the shadows".</p>
<p> We provide Django management commands that are needed to populate the database with data. </p>
<ol>
    <li> 
        <code> ./manage.py parse_excel_data</code> - 
        fetches data from Excel sheets and populates the database 
        with information about mining gear and the pool server 
        locations on different dates.
    </li>
    <li>
        <p>
            <code> ./manage.py start_block_fetching</code> -
            once data about pools and gear is in DB, this command will populate the DB
            with emissions and electricity usage data calculated for time period from 2021-01-01 up until today.
        </p>
        <p>
            <code> --fetch_for_last_24h </code> option fetches the data for the previous day <b>only</b>. 
        </p>
    </li>
    <li>
        <code> ./manage.py remove_all_from_db</code> -
        in case you messed up the setup of your DB or need to start from scratch, 
        this command quickly removes everything from DB, which is useful in development or while doing first-time deployment.
    </li>
    <p>
        To populate the DB, run: <code> ./manage.py parse_excel_data && ./manage.py start_block_fetching </code>
    </p>
    <p>
        Once the population part has ended, you can start querying the API at
        the <code>/calculator/co2_and_electricity_date_range/?start=2021-01-01&end=2021-01-07&format=json</code> endpoint
        with the ability to change the dates to your needs.
    </p>
</ol>
<h2> Production </h2>
<p> 
    In production, the API runs on Apache2 using 
    <code>django_project.conf</code> configuration file 
    (in case you need to change something there).</p>
<p> 
    To execute everyday fetching, we use <code>crontab</code> to run 
    <code> ./manage.py start_block_fetching --fetch_for_last_24h</code>,
    which fetches the data for the day that has just ended (crontab is configured to do so on 12:05 am
    every day). This helps to make API stay up-to-date with new blocks being generated.
</p>