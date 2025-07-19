# CA-GPT-Free v9

**CA-GPT-Free v9** is a production-ready, multi-tenant, open-source automation platform for Chartered Accountancy firms. It is built on a modern, secure, and scalable microservices architecture, designed to be deployed effortlessly using Docker and GitHub Codespaces.

The system's core philosophy revolves around 100% data isolation, production-grade security, data integrity, and complete auditability, all while leveraging a locally-hosted, zero-cost AI for intelligent document processing and summarization.

## ✨ Features

*   **Multi-Tenant by Design:** Secure data isolation between different companies is enforced at the database level.
*   **Granular RBAC:** Flexible Role-Based Access Control system with an Admin UI to manage roles and permissions.
*   **Secure Authentication:** Implements JWT with a secure refresh token rotation strategy (HttpOnly cookies for web, SecureStore for mobile).
*   **Zero-Cost AI:** Integrated with a local Ollama instance (running Mistral) for NLP, OCR, and summarization tasks. AI prompts are customizable per-tenant by Admins.
*   **Data Integrity:** Guarantees atomic transactions for all financial operations and uses optimistic concurrency control to prevent race conditions.
*   **Idempotent APIs:** Protects against duplicate requests and ensures operations are executed exactly once.
*   **Full Audit Trail:** Logs every critical action for compliance and security monitoring.
*   **High-Quality PDF Reporting:** Generates pixel-perfect financial reports (Balance Sheet, P&L) with company branding.
*   **Developer-Friendly:** One-command setup in GitHub Codespaces, centralized logging with correlation IDs, and a comprehensive test suite.

## 🚀 Getting Started (in GitHub Codespaces)

The fastest way to get started is by using GitHub Codespaces.

1.  **Open in Codespaces:** Click the "Code" button on the GitHub repository page and select "Create codespace on main".
2.  **Wait for Initialization:** The Codespace will open in your browser and automatically start building the development container. This might take a few minutes.
3.  **Run Setup:** Once the terminal is available, run the master setup command:

    ```bash
    make setup
    ```

    This single command will:
    *   Build all the Docker images for the services (`server`, `engine`, `ai-service`).
    *   Start all services, including MongoDB and Ollama.
    *   Install all `npm` and `poetry` dependencies.
    *   Pull the `mistral` model for Ollama.
    *   Run the initial database migrations to seed required data.

4.  **Access the Application:**
    *   **API Gateway:** `http://localhost:4000`
    *   **Web Client (Expo):** `http://localhost:8081`
    *   **Engine Service:** `http://localhost:8000`
    *   **AI Service:** `http://localhost:8001`

    GitHub Codespaces will automatically forward these ports for you. You can manage them in the "PORTS" tab.

## 🛠️ Development

### Makefile Commands

This project uses a `Makefile` for simplifying common tasks.

*   `make setup`: The initial, one-time setup command.
*   `make dev`: Starts all services and tails their logs. This is the primary command for day-to-day development.
*   `make up`: Starts all services in detached mode.
*   `make down`: Stops and removes all running containers and volumes.
*   `make logs`: Tails the logs of all running services.
*   `make test`: Runs the test suites for `server`, `engine`, and `ai-service`.
*   `make migrate`: Runs any new database migrations.
*   `make clean`: A destructive command that stops services and removes all Docker images and volumes associated with the project.

### Creating a User

1.  Navigate to the web client (`http://localhost:8081`).
2.  You will be redirected to the login page. Since there are no users yet, use the link or a dedicated button to "Register a new Company".
3.  The registration form will create the first company, the first admin user for that company, and the default set of roles and permissions for that company.
4.  After registration, you will be automatically logged in and redirected to the dashboard.

## 🧪 Testing

To run the complete test suite across all backend services:

```bash
make test