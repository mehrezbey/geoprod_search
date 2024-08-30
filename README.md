# geoprod_search

## Overview
This project is designed to integrate the Geoprod CRM with Elasticsearch. It allows dynamic ingestion of tables from a relational database management system (RDBMS) into Elasticsearch, providing high-performance search capabilities. The project also includes scheduled tasks to maintain coherence between the RDBMS and Elasticsearch by indexing changes periodically.

## Features
- **Dynamic Table Ingestion**: Easily configure which tables to ingest into Elasticsearch via an environment file.
- **Bulk Indexing**: Efficiently index large volumes of data using bulk operations.
- **Scheduled Index Updates**: Maintain data coherence between the RDBMS and Elasticsearch by indexing updates at regular intervals using Celery, RabbitMQ, and APScheduler.
- **High-Performance Search**: Provide web services for fast and accurate search queries through Elasticsearch.

## Technologies Used
- **Python**
- **Flask**: Web framework for building the application.
- **Elasticsearch**: Search and analytics engine for indexing and querying data.
- **Kibana**: Visualization tool for Elasticsearch.
- **Celery**: Distributed task queue for managing background jobs.
- **RabbitMQ**: Message broker used by Celery.
- **MariaDB**: Relational database for storing data.
- **APScheduler**: Task scheduler for running periodic jobs.
- **Docker**
- **Swagger**: 

## Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Docker
- Docker-compose

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/mehrezbey/geoprod_search
   cd geoprod_search```
2. **Run the repository:**
   ```bash
   docker-compose up --build```
3. **Access this URL to search documents :**
    http://172.19.0.5:5000
## Usage
Ingesting Tables into Elasticsearch
Tables to be indexed can be specified in the .env file. The application will dynamically ingest these tables into Elasticsearch, creating indexes as needed.

## Scheduling Index Updates
The application uses Celery, RabbitMQ, and APScheduler to schedule periodic tasks that keep Elasticsearch in sync with the RDBMS. This ensures that any changes in the database are reflected in Elasticsearch without manual intervention.

## Web Services
The application provides RESTful web services for querying Elasticsearch. These services enable high-performance searches across the indexed data.

## Configuration
You can follow the .envexample to  configure the  environment variables.

## Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.


Contact
For questions or further information, please contact:

email : mahrezbey@gmail.com
GitHub: mehrezbey