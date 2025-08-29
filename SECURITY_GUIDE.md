# Security Guide for SeatScape

## Handling Sensitive Information

### GitHub Push Protection Issue

You recently encountered a GitHub push protection issue because sensitive API keys (specifically a Stripe Test API Secret Key) were committed to the repository. This is a security risk as these keys should never be stored in version control.

### How to Fix

1. **Environment Variables**: Always use environment variables for sensitive information
   - The `settings.py` file has been updated to load all Stripe keys from environment variables
   - Make sure to set these variables in your `.env` file (not in version control)

2. **Using the .env File**:
   - Copy the `.env.example` file to a new file named `.env`
   - Fill in your actual API keys and other sensitive information
   - Make sure `.env` is in your `.gitignore` file to prevent it from being committed

3. **Fixing the Git History**:
   - The sensitive keys are still in your Git history in commit `392b16d84832e104d8af3b6ffdd31bcce21ac0fe`
   - You have two options:
     a. Follow the GitHub URL provided in the error message to allow this specific secret (only if it's a test key)
     b. Remove the secret from Git history (recommended for production keys)

### Removing Secrets from Git History

If you need to remove the secret from Git history:

```bash
# Use the BFG Repo-Cleaner tool (safer than git-filter-branch)
# 1. Install BFG: https://rtyley.github.io/bfg-repo-cleaner/
# 2. Create a text file with the secrets to remove
# 3. Run BFG to clean the repository
bfg --replace-text secrets.txt

# Or use git filter-branch (more complex)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch eventbooking/settings.py" \
  --prune-empty --tag-name-filter cat -- --all
```

### Best Practices for API Keys

1. **Never hardcode sensitive information** in your source code
2. **Use environment variables** for all sensitive data
3. **Rotate API keys** regularly, especially after accidental exposure
4. **Use different API keys** for development, testing, and production
5. **Restrict API key permissions** to only what's necessary

### Additional Resources

- [GitHub Secret Scanning Documentation](https://docs.github.com/code-security/secret-scanning/about-secret-scanning)
- [Stripe API Security Best Practices](https://stripe.com/docs/security/guide)
- [Django Security Best Practices](https://docs.djangoproject.com/en/stable/topics/security/)