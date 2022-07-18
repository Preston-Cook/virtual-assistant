# A Conversational AI Bot Created By Preston Cook


## Project Overview

As my final project for CS50, Harvard University's on-campus and online introductory computer science course, I programmed a conversational AI bot designed to interact with users and gather information from the web using a variety of application programming interfaces (APIs). 

In all, the AI bot has the ability to chat with the user in a believable manner, gather location information, send text messages, send emails, retrieve information on trending news headlines, search the web for articles on topics of the user's choice, collect weather information on the user's current location, find recipes, manange a database of contacts, and more. 

In order to perform these tasks, the AI bot makes use of the APIs listed below:
- Assembly AI's Real-Time Speech Recognition API
- Open AI's GTP3 API
- Open Weather's Current Weather Data API
- Google's Text-to-Speech API
- Google's Geolocation API
- Twilio's texting API
- News API
- The Movie Database API

In total, the project consists of 12 local modules, 16 built-in or third-party modules, and a SQLite database to manage contact information.

# Obstacles

Natural language processing is a notoriously tricky task, and its implemntation in this project was no exception. After deciding to add additional functionality on top of Open AI's GTP3 API, I ran into countless issues invloving the order of user's words. 

For instance, suppose someone wanted to send a text to someone named John. They might say, "I'd like to send an email to John" or "Send an email to John". In this case, both phrases are different, yet carry the same meaning. I initially thought I could split the string into an array of words, locate the index of "to", and add one to find the subject. This was fine until someone said "I'd like to send an email to John". In this case, the AI bot would notify me that it failed to find a contact named "email" within its internal database. I ultimately (partially )solved this issue when I reversed the array and subtracted one from the index of "to". The majority of the time, the user will specify the recipient at the end of the sentence, not the beginning.

# Conclusion

Overall, CS50 was a fantastic computer science course that taught me the fundamentals of computer science in a freeing, non-hand-holding way. By providing students with the tools to operate across a wide domain of computer science, learners are encouraged to explore the field and use their creativty to design projects they find interesting. With the knowledge I've gained from this course, the world of tech seems much less daunting, and I look forward to continuing my journey for many years to come. 

This was CS50!
