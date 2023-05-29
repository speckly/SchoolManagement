# About 
This README is written by Andrew Higgins

SchoolManagement is a program developed by 4 first-year GCE Ordinary Level Computing students for teachers to create and access student information in a database, and for students to access programming FAQ.

#Details
This program utilizes a UTF-8 text file to create student information, accessing a student's information while being able to amend or delete it.
Access to the database requires a passcode, to prevent unauthorized access.
The text file is also encrypted using 3 methods. (String indexing, Base64 encoding, Caesar's cipher or ASCII shifting)
The text file is decrypted into plain text while an authorized user is using the database
A student FAQ is included to answer student FAQs on Python (does not require any authentication)

# Author's note 2023
There is so much bad code and unnecessary screaming comments as loud as SQL. I want to preserve this code just for keepsake on the time I was learning software development and managing other people in such projects.

# Security, data encryption - by Andrew Higgins (me)
A security passcode is required to be set should the program be used for the first time (case when file does not exist)
A security question is also required to be set during this initialization which is needed to be answered in the event the authenticated user forgets their password

The security passcode is prompted for every instance a user accesses the database.

### Initialization
![initialization](https://user-images.githubusercontent.com/60218942/125153382-d8da0980-e185-11eb-9199-d90af05d03b4.PNG)

### Security
![security](https://user-images.githubusercontent.com/60218942/125153391-e7282580-e185-11eb-8734-237a17941163.PNG)


The decryption function will be called to convert the database into plain text when the user is authenticated successfully
The encryption function will be called when the user exits a function in the database 
### Sample decrypted data 
![search](https://user-images.githubusercontent.com/60218942/125153288-45a0d400-e185-11eb-8f50-9f8cb647858f.PNG)

### Encrypted data after leaving function 
![encrypted](https://user-images.githubusercontent.com/60218942/125153353-ae884c00-e185-11eb-813f-8fa23aade92b.PNG)

##### Known exploits
- The text file is not stored in a secure location, it can be deleted by an intruder. The intruder can also set a new password without authorization.
- Any interrupts before ```encryption()``` is called might expose database information in plain text. (calling ```decryption()``` while in plain text will return the same plain text)

# Chatbot - Person 2
The chatbot will print out a menu that students can navigate to find their FAQ section 
The chatbot will answer the questions students have on programming based on keywords from their input
![chatbot](https://user-images.githubusercontent.com/60218942/125153978-1345a580-e18a-11eb-88ea-0fd67797416f.PNG)

# Database - Person3/4
The database manages student information by creating, searching, amending and deleting

#### This is how data is created (using the same set of data in a single run)
![create](https://user-images.githubusercontent.com/60218942/125154055-9830bf00-e18a-11eb-82d6-bd0d6d250c0c.PNG)

There cannot be any duplicate students of the same class and index number
![create_lim](https://user-images.githubusercontent.com/60218942/125154096-e80f8600-e18a-11eb-9908-82672913a2f7.PNG)

The data can be accessed later on 
#### Refer to sample decrypted data for screenshot of searched data (unchanged)

# Using this program
You may download ```BUSINESS_MANAGEMENT.py``` and run it as long as you have Python installed
