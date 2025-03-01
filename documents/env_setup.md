# Project Credentials Setup Guide

This document provides step-by-step instructions on how to obtain the necessary API keys and credentials for running the project.

## 1. Google API Key
To obtain a Google API Key:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **APIs & Services > Credentials**.
4. Click **Create Credentials** and select **API Key**.
5. Copy the generated API key and add it to your `.env` file:
   ```
   GOOGLE_API_KEY=your-google-api-key
   ```

## 2. Google Service Account Credentials
To get the `google_service_cred.json` file:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **IAM & Admin > Service Accounts**.
3. Click **Create Service Account** and assign necessary roles.
4. Under **Keys**, click **Add Key > JSON**, and download the file.
5. Rename json file to **google_service_cred.json**
6. Move the file to the `cred_files` directory and set the path in `.env`:
   ```
   GOOGLE_CREDENTIALS_FILE=cred_files/google_service_cred.json
   ```

## 3. Google OAuth Client Secret
To get the `client_secret.json` file:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **APIs & Services > Credentials**.
3. Click **Create Credentials** and choose **OAuth Client ID**.
4. Configure the consent screen and create credentials for **Web Application** or **Desktop Application**.
5. Before download please go to any of **OAuth 2.0 Client IDs** then **Data Access** for adding scopes. 
5. Download the client secret file and rename json file to **client_secret.json**.
6. Move it to the `cred_files` directory and update `.env`:
   ```
   CLIENT_SECRET_FILE=cred_files/client_secret.json
   ```

## 4. Google Sheets ID
To get the Google Sheet ID:
1. Open your Google Sheet.
2. Copy the **spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/your-sheet-id/edit
   ```
3. Add it to `.env`:
   ```
   SHEET_ID=your-sheet-id
   ```

## 5. Gmail User Email
To set up Gmail API:
1. Enable **Gmail API** in Google Cloud Console.
2. Add your Gmail email in `.env`:
   ```
   GMAIL_USER_EMAIL=your-email@gmail.com
   ```

## 6. Hunter.io API Key
To obtain a Hunter API key:
1. Sign up at [Hunter.io](https://hunter.io/).
2. Navigate to **API** and copy your API key.
3. Add it to `.env`:
   ```
   HUNTER_API_KEY=your-hunter-api-key
   ```

## 7. OpenAI API Key
To get an OpenAI API Key:
1. Go to [OpenAI API](https://platform.openai.com/signup/).
2. Sign in and navigate to **API Keys**.
3. Create a new key and add it to `.env`:
   ```
   OPENAI_API_KEY=your-openai-api-key
   ```
## 8. Finalizing the Setup
1. Ensure your `.env` file contains necessary all the required variables.
2. Place all JSON credential files inside the `cred_files` directory.
3. Run the script to verify configuration:
   ```
   python verify_config.py
   ```

This ensures all credentials are correctly set up for the project. 

