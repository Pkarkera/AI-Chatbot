# AI-Chatbot

## Overview

This project is a chatbot built using Python and Flask that leverages the Google Gemini API to generate responses based on user queries. The chatbot can read and process PDF textbooks, providing intelligent answers to questions asked by users.

## Features

    A. Interactive chatbot UI

    B. Google Gemini API integration for AI-driven responses

    C. PDF textbook processing for context-aware answers

    D. Flask-based backend for efficient request handling

## Technologies Used

    A. Backend: Python, Flask

    B. AI Integration: Google Gemini API

    C. Frontend: HTML, CSS, JavaScript

    D. PDF Processing: PyMuPDF (fitz)

## Installation

### Prerequisites

1. Ensure you have the following installed:

    a. Python 3.x

    b. Flask

    c. PyMuPDF

## Setup

### Clone the repository:

  git clone https://github.com/Pkarkera/AI-Chatbot

### Install dependencies:

  1. Set up your Google Gemini API key in a .env file:

    GEMINI_API_KEY=your_api_key_here

  2. Run the Flask server:

    python app.py

  3. Open the application in your browser at http://localhost:5003.

## Usage

  1. Upload a PDF textbook.

  2. Ask questions related to the uploaded document.

  3. The chatbot will provide context-aware responses.

## Future Enhancements

  1. Improve chatbot accuracy with better context retrieval.

  2. Add support for multiple PDF uploads.

  3. Enhance UI for a more interactive experience.
