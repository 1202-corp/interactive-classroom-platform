#!/bin/bash
# Script to create DNS instructions README in smtp-keys after DKIM keys are generated
# This script should be run after the first postfix container start

set -e

DOMAIN="${SMTP_DOMAIN:?SMTP_DOMAIN is required}"
KEYS_DIR="${KEYS_DIR:-/smtp-keys}"
# boky/postfix writes keys as keys/DOMAIN.txt (not keys/DOMAIN/DOMAIN.txt)
TXT_FILE="${KEYS_DIR}/${DOMAIN}.txt"
README_FILE="${KEYS_DIR}/README-DNS.md"

# Wait for keys to be generated (with timeout)
MAX_WAIT=60
WAITED=0
while [ ! -f "$TXT_FILE" ] && [ $WAITED -lt $MAX_WAIT ]; do
    echo "Waiting for DKIM keys to be generated... ($WAITED/$MAX_WAIT seconds)"
    sleep 2
    WAITED=$((WAITED + 2))
done

if [ ! -f "$TXT_FILE" ]; then
    echo "ERROR: DKIM key file not found: $TXT_FILE"
    echo "Postfix container may not have generated keys yet. Check container logs:"
    echo "  docker logs smtp-postfix"
    exit 1
fi

# Extract the TXT record content from the .txt file
TXT_RECORD=$(grep -v "^;" "$TXT_FILE" | tr -d '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

# Create README with DNS instructions
cat > "$README_FILE" <<EOF
# DKIM DNS Setup Instructions

## Domain: ${DOMAIN}

After the postfix container has generated DKIM keys, add the following DNS TXT record:

### DNS Record

**Record Type:** TXT  
**Name/Host:** \`mail._domainkey\`  
**Value:** (see below)

### TXT Record Value

Copy the entire value below (it's a single long string):

\`\`\`
${TXT_RECORD}
\`\`\`

### Full DNS Entry Example

For domain \`${DOMAIN}\`, add:

\`\`\`
mail._domainkey.${DOMAIN}    IN    TXT    "${TXT_RECORD}"
\`\`\`

### Verification

After adding the DNS record, wait for DNS propagation (can take a few minutes to hours), then verify:

1. Check DNS propagation:
   \`\`\`bash
   dig TXT mail._domainkey.${DOMAIN}
   \`\`\`

2. Test email signing:
   - Send a test email from your application
   - Check email headers for DKIM signature
   - Use a DKIM validator like https://dkimvalidator.com/

### Notes

- The DKIM selector is \`mail\` (default)
- Private key: \`${KEYS_DIR}/${DOMAIN}.private\` (keep secure, do not share)
- Public key (DNS): \`${KEYS_DIR}/${DOMAIN}.txt\`

### Regenerating Keys

If you need to regenerate keys:
1. Stop the postfix container
2. Delete \`${KEYS_DIR}/${DOMAIN}.private\` and \`${KEYS_DIR}/${DOMAIN}.txt\`
3. Restart the container - keys will be regenerated automatically
4. Update the DNS record with the new TXT value

EOF

echo "✓ DNS instructions created: $README_FILE"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DKIM DNS TXT Record for domain: ${DOMAIN}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Record Type: TXT"
echo "Name/Host: mail._domainkey"
echo "Full Name: mail._domainkey.${DOMAIN}"
echo ""
echo "TXT Record Value (copy this entire string):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "${TXT_RECORD}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Add the TXT record above to your DNS for: mail._domainkey.${DOMAIN}"
echo "2. Wait for DNS propagation (can take minutes to hours)"
echo "3. Verify with: dig TXT mail._domainkey.${DOMAIN}"
echo ""
echo "Full instructions are also saved in: $README_FILE"
