# Amana Capital EA API Integration

## Overview
This document outlines the API endpoints available for the Enterprise CRM and Client Portal.

## Authentication
All API requests must include a valid JWT token in the `Authorization` header.
`Authorization: Bearer <token>`

## Endpoints

### `GET /api/v1/clients`
Retrieves a list of clients (Admin only).

### `GET /api/v1/portfolio/{client_id}`
Retrieves the portfolio summary for a specific client.
