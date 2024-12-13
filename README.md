# Performance Dashboard

This project is a **Performance Dashboard** built to track and visualize the performance metrics of 200 employees. It utilizes modern technologies and follows best practices for scalable, efficient, and reliable software.

---

## Features

- **Interactive Dashboard**: Built with React and MaterialUI, offering an intuitive and responsive user interface.
- **Data Visualization**: Employs Chart.js for dynamic and visually appealing charts.
- **Backend API**: Powered by Flask with Pydantic for data validation and a MySQL database.
- **Containerization**: Utilizes Docker and Docker Compose for a consistent deployment environment.
- **CI/CD**: Integrated GitLab pipelines to automate testing, building, and deployment.
- **MVC Design Pattern**: Organized architecture to ensure maintainability and scalability.

---

## Technology Stack

### Frontend:
- **React**: For building the user interface.
- **MaterialUI**: For styling and components.
- **Chart.js**: For rendering performance data charts.

### Backend:
- **Flask**: For REST API development.
- **Pydantic**: For data validation and serialization.
- **MySQL**: Database to store and query performance metrics.
- **PyTest**: For unit tests.

### Deployment:
- **Docker**: For containerization.
- **Docker Compose**: To simplify multi-container setup.
- **GitLab CI/CD**: For continuous integration and deployment pipelines.

---

## Prerequisites

Ensure the following software is installed on your system:
- Docker
- Docker Compose
- MySQL

---

## How to Run

### Using Docker Compose:

1. Clone this repository:
    ```bash
    git clone https://github.com/hiepnguyenduc2005/dashboard-intern.git
    cd dashboard-intern
    ```
2. Add environment variables, then build and start the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```
The frontend will be available at http://localhost:3000 and the backend API at http://localhost:5000.

### Without Docker:
1. Install backend dependencies:
    ```bash
    cd server
    pip install -r requirements.txt
    ```
2. Set up the MySQL database and configure the .env file in the backend folder.
3. Start the Flask server:
    ```bash
    python app.py
    ```
4. Install frontend dependencies:
    ```bash
    cd client
    npm install
    ```
5. Start the React client:
    ```bash
    npm run dev
    ```
---
## CI/CD
This project includes a GitLab CI/CD pipeline that automates:
- Testing for backend and frontend.
- Building Docker images.
- Deploying the application to the desired environment.
To set up GitLab CI/CD, ensure the .gitlab-ci.yml file is configured with your Docker registry and deployment environment details.

---
## Contribution
Contributions are welcome! Please fork the repository and create a pull request with your changes.

---
## License
This project is licensed under the MIT License. See LICENSE for details.

---
## Contact
For any queries or suggestions, feel free to reach out via the project repository.
Let me know if you'd like further customization!
