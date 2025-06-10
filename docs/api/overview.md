# API Reference Overview

This section provides detailed information about the API Auth service endpoints, authentication methods, and response formats.

## Base URL

The base URL for all API endpoints is:

```
https://api.karned.bzh/auth/
```

For local development, the base URL is:

```
http://localhost:8000/
```

## API Versions

The API Auth service supports multiple API versions:

- **v1**: Current stable API

To specify the API version, include it in the URL path:

```
https://api.karned.bzh/auth/v1/
```

## Authentication

All API endpoints require authentication. The API Auth service supports the following authentication methods:

### Obtaining a Token

To obtain an authentication token, send a POST request to the `/auth/v1/token` endpoint with your credentials:

```
POST /auth/v1/token
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

The response will include an access token and a refresh token:

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5...",
  "token_type": "bearer",
  "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5..."
}
```

### Renewing a Token

To renew an expired access token without re-authenticating with username and password, send a POST request to the `/auth/v1/renew` endpoint with your refresh token:

```
POST /auth/v1/renew
Content-Type: application/json

{
  "refresh_token": "your_refresh_token"
}
```

The response will include a new access token and refresh token:

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5...",
  "token_type": "bearer",
  "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5..."
}
```

## Response Format

All API responses are in JSON format. A typical response has the following structure:

```json
{
  "status": "success",
  "data": {
    // Response data
  },
  "message": "Operation completed successfully"
}
```

### Error Responses

Error responses have the following structure:

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message"
  }
}
```

## Next Steps

- Visit our [Swagger Documentation](https://api.karned.bzh/auth/docs) for interactive API testing and exploration.
