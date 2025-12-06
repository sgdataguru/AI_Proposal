# Quick Start: Testing Gamma MCP Server with 10 Parameters

This guide walks through testing the `generate-presentation` tool with the full 10-parameter payload.

## Step 1: Setup

```bash
# Navigate to gamma-mcp-server directory
cd gamma-mcp-server

# Install dependencies (if not already done)
npm install
```

## Step 2: Run Validation Tests

These tests verify schema validation without needing an API key:

```bash
# Run comprehensive 10-parameter test suite
node test-10-params.mjs
```

**Expected Output:**
```
🧪 Gamma MCP Server - 10 Parameter Test Suite
✅ PASS: Test 1.1: Valid 10-parameter payload (corrected enums)
✅ PASS: Test 1.2: Valid minimal payload (only inputText)
...
Total Tests: 13
✅ Passed: 13
❌ Failed: 0
🎉 All tests passed!
```

## Step 3: Verify Server Startup

### Test without API key (should fail fast):
```bash
npx tsx src/index.ts
```

**Expected Output:**
```
ERROR: GAMMA_API_KEY environment variable is not set.
Please add your Gamma API key to the .env file.
```

### Test with API key (should start):
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your API key:
# GAMMA_API_KEY=your_actual_key_here

# Start server
npm run dev
```

**Expected Output:**
```
Gamma MCP Server running on stdio
```

Press Ctrl+C to stop.

## Step 4: (Optional) Test with Live API

If you have a valid Gamma API key:

1. Add it to `.env`:
   ```
   GAMMA_API_KEY=your_actual_gamma_api_key
   ```

2. Run the test suite again:
   ```bash
   node test-10-params.mjs
   ```

3. The API integration test will execute and return a presentation URL.

## Step 5: (Optional) Test with Claude Desktop

### Configure Claude Desktop

1. Locate your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Add the Gamma MCP server:
   ```json
   {
     "mcpServers": {
       "gamma": {
         "command": "npx",
         "args": [
           "tsx",
           "/absolute/path/to/AI_Proposal/gamma-mcp-server/src/index.ts"
         ],
         "env": {
           "GAMMA_API_KEY": "your_actual_api_key_here"
         }
       }
     }
   }
   ```

3. Replace `/absolute/path/to/AI_Proposal` with your actual path

4. Restart Claude Desktop completely

### Test in Claude Desktop

Ask Claude:
> "Create a presentation about AI in healthcare with 12 slides. Use a professional tone, target healthcare executives, and include photographic images."

Claude should:
1. Recognize the `generate-presentation` tool
2. Call it with appropriate parameters
3. Return a Gamma presentation URL

## Verification Checklist

After running the tests, verify:

- [ ] All 13 validation tests pass
- [ ] Server fails fast without API key with clear error message
- [ ] Server starts successfully with API key
- [ ] No API keys or secrets visible in test output
- [ ] Invalid enum values are rejected with helpful error messages
- [ ] Valid 10-parameter payload passes validation
- [ ] .env file is not committed to git (check .gitignore)

## Test Coverage

The test suite validates all 10 parameters:

1. ✅ **inputText** (required) - Main content prompt
2. ✅ **tone** - professional | casual | enthusiastic | informative
3. ✅ **audience** - Target audience description
4. ✅ **textAmount** - concise | balanced | detailed
5. ✅ **textMode** - auto | cards | bullets | paragraphs
6. ✅ **numCards** - Integer between 1-50
7. ✅ **imageModel** - dalle2 | dalle3 | sdxl
8. ✅ **imageStyle** - photographic | digital_art | illustration | 3d_render
9. ✅ **editorMode** - present | card | doc
10. ✅ **additionalInstructions** - Extra generation instructions

## Valid Example Payload

```json
{
  "inputText": "AI Lead Scoring & Activation for wealth management in India: a 5-week PoC roadmap",
  "tone": "professional",
  "audience": "wealth RMs and business stakeholders",
  "textAmount": "balanced",
  "textMode": "bullets",
  "numCards": 12,
  "imageModel": "dalle3",
  "imageStyle": "photographic",
  "editorMode": "present",
  "additionalInstructions": "Include a simple architecture slide, a 5-week timeline, and a governance-by-design checklist."
}
```

## Troubleshooting

### "Cannot find package 'zod'"
- Make sure you're in the `gamma-mcp-server` directory
- Run `npm install`

### "API test is skipped"
- This is expected if GAMMA_API_KEY is not configured
- Schema validation tests still verify everything works correctly
- To test API calls, add your API key to `.env`

### "Module not found" errors
- Ensure you're using Node.js 18 or higher: `node --version`
- Run `npm install` to ensure all dependencies are installed

### Claude Desktop doesn't see the tool
- Use absolute paths (not `~/`) in the config
- Completely quit and restart Claude Desktop
- Check Claude Desktop logs for errors

## Next Steps

After successful testing:
1. Review TEST_EVIDENCE.md for detailed test documentation
2. Check README.md for full usage documentation
3. See SECURITY.md for security best practices

## Support

For issues:
- Review the Troubleshooting section in README.md
- Check test output for specific error messages
- Verify enum values match the schema exactly
