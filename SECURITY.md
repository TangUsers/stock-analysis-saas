# Security Policy

## Supported Versions

We currently support the following versions of the project with security updates:

| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Yes    |
| 0.x     | ❌ No     |

## Reporting a Vulnerability

We take the security of our project seriously. If you believe you have found a security vulnerability, please report it to us responsibly.

### How to Report

1. **Do NOT** open issue on GitHub
 a public2. Email your report to: **security@openclaw.dev**
3. Include in your report:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Your contact information (optional)

### What to Expect

After you submit your report:

1. We will acknowledge receipt within 24-48 hours
2. We will investigate and validate the vulnerability
3. We will keep you informed of our progress
4. Once fixed, we will credit you in our security advisories (if you wish)

## Security Best Practices

When using or contributing to this project, please follow these security guidelines:

### For Users

- Keep your installation up to date with the latest release
- Do not expose API endpoints publicly without proper authentication
- Use environment variables for sensitive configuration
- Regularly rotate API keys and tokens
- Review logs for suspicious activity

### For Contributors

- Never commit sensitive data (API keys, passwords, tokens)
- Use environment variables for all secrets
- Review code for potential security issues before submitting PRs
- Follow secure coding practices
- Use parameterized queries to prevent SQL injection
- Validate all input data

## Security Features

This project includes:

- Input validation using Pydantic
- Secure password handling
- CORS configuration
- Environment-based configuration

## Dependencies

We regularly update dependencies to address security vulnerabilities:

- Run `pip-audit` or similar tools to check for vulnerable dependencies
- Enable Dependabot for automatic security updates
- Review security advisories for all dependencies

## Disclaimer

This project is provided "as is" without warranty. Use at your own risk. The maintainers are not liable for any damages or losses resulting from the use of this software.

---

**Thank you for helping keep Stock Analysis SaaS secure!**
