This document outlines the key aspects of the Django project, as understood by the Gemini CLI assistant.

## Project Overview

The project is a Django application named 'emza' designed for managing inventory, products, and sales. It appears to be an application for a small business, possibly one that sells custom products made from various stock components, like perfumes. The project is also configured as a Progressive Web App (PWA).

## Core Applications

The project is divided into several Django apps:

-   `main`: A core app, but currently without any models.
-   `stock`: Manages the raw materials or stock items.
-   `product`: Manages the final products that are sold.
-   `sale`: Manages sales transactions and billing.
-   `customer`: Manages customer information.
-   `pwa`: Handles the Progressive Web App configuration.

## Data Models

### Stock App (`stock`)

-   **`StockType`**: Defines the type of stock and its unit of measurement (e.g., "Perfume" in "ml", "Bottle" in "pcs").
-   **`Stock`**: Represents an individual stock item, tracking its quantity on hand. It has methods to handle purchases, sales, and returns of stock.

### Product App (`product`)

-   **`Product`**: Represents a final product for sale. Its available quantity is dynamically calculated based on the availability of its components (defined in `StockVariant`). It has methods to manage the stock reduction/increase when a product is sold or returned.
-   **`StockVariant`**: A through model that defines the bill of materials for a product. It links a product to the stock items required to create it and specifies the quantity of each stock item needed.

### Customer App (`customer`)

-   **`Customer`**: A simple model to store customer information, including name, phone number, and address.

### Sale App (`sale`)

-   **`SaleBill`**: Represents a sales bill, which is linked to a customer. It automatically generates a bill number and calculates the total amount.
-   **`ProductSale`**: Represents a line item on a `SaleBill`, linking a product, quantity, and price. It includes validation to prevent selling more than the available quantity and updates the stock levels upon saving. A signal is used to restock items if a sale is deleted.

## Deployment

The project includes `vercel.json` and `build.sh`, which suggests it is set up for deployment on the Vercel platform. The `build.sh` script likely handles the installation of dependencies and database migrations.

## Authentication

The project uses Django's built-in authentication system, with login and logout URLs configured. The `LOGIN_REDIRECT_URL` is set to `/sales`, indicating that users are directed to the sales page after logging in.
