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
