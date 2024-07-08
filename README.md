# Backend Application

## Overview
This repository contains a backend application designed to handle CSV data uploads and perform data analysis based on various filters. The application is built with the following features:

## API:

1. Upload CSV data
2. Analyze data based on filters

## Database:

1. Store the CSV data
2. SQLite
   
## Deployment:

1. Created a Docker image for easy deployment
2. Deploy the system to a free tier of any cloud provider for analysts to try(Railway)

## Bonus Features:

1. Simple authentication to restrict API access (token based)
2. Simple UI to query data(https://glytics-frontend.vercel.app/)
3. Support for aggregate searches (e.g., records where total (x) > 100, get max/min/mean value of a numerical column)

## API Endpoints
### Upload CSV Data
Endpoint: /upload_csv
Method: POST
Description: Upload a CSV file to be stored in the database.

### Query Data
Endpoint: /query
Method: GET
Description: Retrieve and analyze data using specified filters.

## Database
The application supports storing CSV data in SQLite.

## Deployment
The application can be easily deployed using Docker. Follow the steps below to build and run the Docker image:

### Build Docker Image
bash

`docker build -t glytics-backend`

### Run Docker Container
bash

`docker run -d -p 8000:8000 glytics-backend`

## How to Use
## Clone the Repository:

bash

`git clone https://github.com/HarshDeswal/glytics-backend.git`
`cd glytics-backend`

## Build and Run the Docker Image:

bash

`docker build -t glytics-backend`
`docker run -d -p 8000:8000 glytics-backend`


## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
