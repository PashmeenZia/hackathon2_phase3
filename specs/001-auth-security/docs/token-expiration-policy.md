# JWT Token Expiration Policies

## Overview
The authentication system implements time-based security controls through configurable JWT token expiration policies. This ensures that authentication tokens have limited validity periods, reducing the security risk associated with long-lived tokens.

## Token Types and Expiration
- **Access Tokens**: Short-lived tokens with configurable expiration (default: 30 minutes)
- **Token Format**: `Authorization: Bearer <JWT>`

## Configuration
Token expiration is configured via environment variables:

```
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Security Implications
- **Limited Exposure Window**: If a token is compromised, it becomes invalid after the expiration period
- **Forced Re-authentication**: Users must re-authenticate after token expiration
- **Reduced Replay Attack Risk**: Expired tokens cannot be reused

## Behavior
- Tokens expire automatically after the configured time period
- Expired tokens result in 401 Unauthorized responses when used
- Applications should implement automatic token refresh mechanisms
- Server-side validation occurs on every protected request

## Best Practices
- Keep access token lifetimes relatively short (15-60 minutes)
- Implement secure token refresh mechanisms for better UX
- Monitor token usage patterns for security analysis
- Log authentication failures for security monitoring