**Translation AI Service** is an asynchronous web application that allows users to input text for translation into several different languages. 
Leveraging OpenAI's API, this application processes user requests in an efficient manner, storing the translated text in a database and allowing
 users to check the status and content of their translation tasks at any time.

## Features

- **Asynchronous Translation**: Users can submit text for translation while the application processes requests in the background.
- **Multi-Language Support**: Translate text into multiple languages.
- **Task Management**: Each translation task is assigned a unique ID for tracking.
- **Database Storage**: Translated text and its status are stored in a PostgreSQL database.
- **OpenAI Integration**: Uses OpenAI's API to perform translations using ChatGPT.
- **JSON Output**: The output of translated text is displayed in JSON format.


## Technologies Used

- **Backend**: FastAPI
- **Database**: PostgreSQL (hosted on Render.com)
- **Asynchronous Handling**: Axiom (from JavaScript)
- **API Integration**: OpenAI ChatGPT API
- **Testing**: Pytest
