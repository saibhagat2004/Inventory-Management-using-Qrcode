# QR Inventory Manager

## Introduction

The QR Inventory Manager is a web-based application designed to streamline inventory management processes using QR code integration. This application allows users to efficiently track products, manage stock levels, and dispatch orders to customers or shops. By leveraging QR codes for product identification and scanning, the system ensures accurate and rapid inventory updates.

## Features

- **QR Code Integration**: Utilizes QR codes for product identification and scanning, enabling quick and accurate inventory management.
- **Product Management**: Allows users to add, edit, and view detailed information about products, including name, brand, model, price, and description.
- **Inventory Tracking**: Provides real-time tracking of product quantities in stock, facilitating efficient inventory control.
- **Order Dispatch**: Enables users to dispatch products to customers or shops, automatically updating stock levels upon dispatch.
- **Customer Management**: Allows users to manage customer information, including name, shop name, and address.
- **Dispatch History**: Displays a history of dispatched products, including dispatch ID, customer ID, shop name, product name, quantity, and timestamp.
- **User-Friendly Interface**: Features a simple and intuitive user interface for easy navigation and interaction.

## Getting Started

To get started with the QR Inventory Manager, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**: Install the necessary dependencies by running `pip install -r requirements.txt`.
3. **Set Up the Database**: Set up the PostgreSQL database and configure the connection string in `app.py`.
4. **Run the Application**: Run the Flask application using `python app.py`.
5. **Access the Application**: Access the application by navigating to `http://localhost:5000` in your web browser.

## Technologies Used

- **Python**: Backend development and business logic.
- **Flask**: Web framework for building the application.
- **SQLAlchemy**: ORM for interacting with the database.
- **PostgreSQL**: Relational database management system for data storage.
- **HTML/CSS**: Frontend markup and styling.
- **JavaScript**: Frontend interactivity and dynamic behavior.
