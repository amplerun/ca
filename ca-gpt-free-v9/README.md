# CA-GPT-Free v9

**CA-GPT-Free v9** is a production-ready, multi-tenant, open-source automation platform for Chartered Accountancy firms. It is built on a modern, secure, and scalable microservices architecture, designed to be deployed effortlessly using Docker and GitHub Codespaces.

The system's core philosophy revolves around 100% data isolation, production-grade security, data integrity, and complete auditability, all while leveraging a locally-hosted, zero-cost AI for intelligent document processing and summarization.

## 🚀 Getting Started (in GitHub Codespaces)

1.  **Open in Codespaces:** This script has already created the project for you.
2.  **Run Setup:** From the root of the `ca-gpt-free-v9` directory, run the master setup command:

    ```bash
    make setup
    ```

    This command will build and start all services, install dependencies, pull the AI model, and run database migrations.

3.  **Access the Application:**
    *   **API Gateway:** `http://localhost:4000`
    *   **Web Client (Expo):** `http://localhost:8081`

    GitHub Codespaces will automatically forward these ports. Check the "PORTS" tab.
