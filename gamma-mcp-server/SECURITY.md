# Security Updates

## Recent Security Fixes

### 2025-12-06: MCP SDK DNS Rebinding Vulnerability

**Vulnerability**: Model Context Protocol (MCP) TypeScript SDK does not enable DNS rebinding protection by default.

**Affected Versions**: @modelcontextprotocol/sdk < 1.24.0

**Status**: ✅ FIXED

**Details**:
- **Original Version**: 0.6.1 (vulnerable)
- **Updated Version**: 1.24.3 (patched)
- **CVE Impact**: DNS rebinding attacks could potentially be used to bypass same-origin policy
- **Fix Applied**: Upgraded dependency to version 1.24.0+ which includes DNS rebinding protection by default

**Verification**:
```bash
$ npm audit
found 0 vulnerabilities
```

**Testing After Fix**:
- ✅ All TypeScript compilation tests passed
- ✅ All validation tests passed (10/10)
- ✅ Server startup verified in dev and prod modes
- ✅ CodeQL security scan: 0 alerts
- ✅ NPM audit: 0 vulnerabilities

**No Breaking Changes**: The SDK upgrade from 0.6.1 to 1.24.3 did not require any code changes. All existing functionality continues to work as expected.

---

## Security Best Practices

This project follows security best practices:

1. **No Secrets in Code**: API keys are managed via environment variables only
2. **Gitignore Configuration**: `.env` files are excluded from version control
3. **Dependency Scanning**: Regular npm audit checks
4. **Static Analysis**: CodeQL security scanning enabled
5. **Fail-Fast**: Server validates configuration on startup
6. **Input Validation**: All tool parameters validated with Zod
7. **Safe Error Handling**: No sensitive data leaked in error messages
8. **Minimal Dependencies**: Only necessary packages included

---

## Reporting Security Issues

If you discover a security vulnerability in this project, please:

1. **Do NOT** open a public issue
2. Report via GitHub Security Advisories (if available)
3. Or contact the repository maintainers directly

We take security seriously and will respond promptly to legitimate security concerns.

---

## Security Checklist for Users

When deploying this MCP server:

- ✅ Store API keys in `.env` file or environment variables (never in code)
- ✅ Keep dependencies up to date (`npm update`)
- ✅ Run `npm audit` regularly to check for vulnerabilities
- ✅ Use the latest stable version of the server
- ✅ Review Claude Desktop configuration for proper path and key management
- ✅ Limit access to the `.env` file (file permissions)
- ✅ Use secure channels when sharing configuration instructions

---

## Dependency Security

Current dependencies and their security status:

| Package | Version | Security Status |
|---------|---------|-----------------|
| @modelcontextprotocol/sdk | ^1.24.3 | ✅ Secure (patched) |
| dotenv | ^16.4.5 | ✅ No known vulnerabilities |
| node-fetch | ^3.3.2 | ✅ No known vulnerabilities |
| zod | ^3.23.8 | ✅ No known vulnerabilities |
| typescript | ^5.7.2 | ✅ No known vulnerabilities |
| tsx | ^4.21.0 | ✅ No known vulnerabilities |

**Last Verified**: 2025-12-06

---

## Automated Security

Recommended security automation:

1. **Dependabot**: Enable GitHub Dependabot for automatic dependency updates
2. **CodeQL**: Enable GitHub CodeQL scanning
3. **NPM Audit**: Add to CI/CD pipeline
4. **Secret Scanning**: Enable GitHub secret scanning

---

## Update History

- **2025-12-06**: Initial security documentation
- **2025-12-06**: Fixed MCP SDK DNS rebinding vulnerability (0.6.1 → 1.24.3)
