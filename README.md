# Cinema Ticket booking
This project is written in python-flask

For ticket booking:

- Very first step is to select the tickets that are available for booking.

- Once you have selected the particular tickets, click on book now button.

- After selecting tickets, Fill in the name, valid email and then click on confirm booking for getting confirmation email for the tickets you selected.

For ticket cancellation:

- Click on the ticket, that you want to cancel.

- Fill the correct email, As it will be cancelled only by that user who has booked it. Then click on unbook. 


## Installation

The installation process is very easy and it includes:

- Clone this repo.

- Create a virtual environment for python3 inside a cloned folder.

- Activate the virtual environment you created.

- Install all the dependencies of requirements.txt, with the help of command given below:

```bash
pip install -r requirements.txt
```
- Create a database in mysql. Also, Configure the database in init.py file.

- For email, Include setup details of your gmail in init.py file.

- To create the database tables. Open the terminal type python and import db from ticketbooking module. Commands are given below:
```bash
from ticketbooking import db
db.create_all()
```
This will create the tables in your database.

Note: Add smtp details in init.py file for sending email.

## To run the program
 ```bash
python run.py
```
The program will run on http://127.0.0.1:5000/

## To run the test cases

Firstly, we need to configure the database which can be done by adding SQL Database URI to test_ticketbooking.py file.

 ```bash
 python test_ticketbooking.py
```
