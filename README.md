
# Madugu Sambo Educational Foundation

<!-----

Yay, no errors, warnings, or alerts!

Conversion time: 0.248 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β34
* Sat Mar 18 2023 09:16:17 GMT-0700 (PDT)
* Source doc: Madugu 
----->



# Record Digita 

This is a web application built with Django 


## Features
The application has the following features:


## Installation
First clone the application form git hub using the command below 
```
git clone https://github.com/
```

To run the application, you need to have Python and Django installed on your machine. You can install the dependencies using the requirements.txt file by running the following command:

Then you configure your .env file with the following variables
Create .env file and add the below things
```
SECRET_KEY=b74fc77676d85d6356d3597e281ea937d81307b0af5e4c76
DB_ENGINE_NAME=sqlite
PLATFORM=dev
DEBUG=True
``` 


```
pip install -r requirements.txt
```


Once the dependencies are installed, you can run the application using the following command:



```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


This will start the development server at[ http://localhost:8000/](http://localhost:8000/). You can access the application by visiting this URL in your web browser.


## Conclusion

