# CS-447-Python-Chat-Application
![logo-removebg-preview (1)](https://user-images.githubusercontent.com/98253476/211147952-30da9711-6df3-444b-b275-f9ca2dd5afe8.png)

  Zaggu is a multiplatform online chat application that you can use to have an anonymous conversation with anyone in the world. Messages are end to end encrypted. Data is only stored for the current session that a user is logged in, once a user leaves the session, their data is deleted along with it. 

  The code for Zaggu creates a chat application written in Python using the Asyncio library, the PYwebio library, and the cryptography library. It makes use of the PBKDF2HMAC function from the cryptography library to generate a secret key for encrypting and decrypting messages sent over the chat. The chat application has a feature for users to enter their name, and it keeps a record of all users who are currently online. It also has a function called refresh_msg which checks for new messages every second and displays them in the chat window.
