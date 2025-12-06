# Gamma MCP Server

An MCP (Model Context Protocol) server that enables AI assistants like Claude to generate presentations using the Gamma API.

## Features

- **Single Tool**: `generate-presentation` - Creates presentations from text prompts
- **Rich Parameters**: Customize tone, audience, text amount, images, and more
- **Secure**: API key management via environment variables
- **Type-Safe**: Built with TypeScript and Zod validation
- **Easy Integration**: Works seamlessly with Claude Desktop and other MCP clients

## Prerequisites

- Node.js 18 or higher
- A Gamma API key (get one from [Gamma](https://gamma.app))

## Installation

1. Clone this repository or navigate to the `gamma-mcp-server` directory:

```bash
cd gamma-mcp-server
```

2. Install dependencies:

```bash
npm install
```

3. Create a `.env` file in the `gamma-mcp-server` directory:

```bash
cp .env.example .env
```

4. Add your Gamma API key to the `.env` file:

```env
GAMMA_API_KEY=your_gamma_api_key_here
```

## Usage

### Running Locally

#### Option 1: Development Mode (TypeScript with tsx)

```bash
npm run dev
```

Or directly with npx:

```bash
npx tsx src/index.ts
```

#### Option 2: Build and Run (Production)

```bash
# Build TypeScript to JavaScript
npm run build

# Run the compiled server
npm start
```

The server will start and listen on stdio, outputting:
```
Gamma MCP Server running on stdio
```

### Tool: generate-presentation

Generates a presentation using the Gamma API.

#### Parameters

- **inputText** (required, string): The main content/prompt for the presentation
- **tone** (optional, enum): Presentation tone
  - Options: `"professional"`, `"casual"`, `"enthusiastic"`, `"informative"`
- **audience** (optional, string): Target audience description
- **textAmount** (optional, enum): Amount of text per slide
  - Options: `"concise"`, `"balanced"`, `"detailed"`
- **textMode** (optional, enum): Text formatting style
  - Options: `"auto"`, `"cards"`, `"bullets"`, `"paragraphs"`
- **numCards** (optional, number): Number of slides (1-50)
- **imageModel** (optional, enum): AI model for image generation
  - Options: `"dalle2"`, `"dalle3"`, `"sdxl"`
- **imageStyle** (optional, enum): Style of generated images
  - Options: `"photographic"`, `"digital_art"`, `"illustration"`, `"3d_render"`
- **editorMode** (optional, enum): Presentation editor mode
  - Options: `"present"`, `"card"`, `"doc"`
- **additionalInstructions** (optional, string): Extra instructions for generation

#### Example Request

```json
{
  "inputText": "Create a presentation about the benefits of artificial intelligence in healthcare",
  "tone": "professional",
  "audience": "Healthcare executives",
  "textAmount": "balanced",
  "numCards": 10,
  "imageStyle": "photographic"
}
```

#### Example Response

```
Successfully generated presentation! View it here: https://gamma.app/docs/...
```

## Claude Desktop Integration

To use this MCP server with Claude Desktop:

### Step 1: Locate Claude Desktop Configuration

The configuration file is located at:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Step 2: Add Server Configuration

Edit the configuration file and add the Gamma MCP server:

#### Using tsx (Development)

```json
{
  "mcpServers": {
    "gamma": {
      "command": "npx",
      "args": [
        "tsx",
        "/absolute/path/to/gamma-mcp-server/src/index.ts"
      ],
      "env": {
        "GAMMA_API_KEY": "your_gamma_api_key_here"
      }
    }
  }
}
```

#### Using Node (Production - after building)

```json
{
  "mcpServers": {
    "gamma": {
      "command": "node",
      "args": [
        "/absolute/path/to/gamma-mcp-server/dist/index.js"
      ],
      "env": {
        "GAMMA_API_KEY": "your_gamma_api_key_here"
      }
    }
  }
}
```

**Important Notes:**
- Replace `/absolute/path/to/gamma-mcp-server` with the actual absolute path on your system
- You can pass the API key via `env` in the config (as shown) OR rely on the `.env` file in the gamma-mcp-server directory
- If using the built version, make sure to run `npm run build` first

### Step 3: Restart Claude Desktop

After updating the configuration, completely quit and restart Claude Desktop for changes to take effect.

### Step 4: Verify Integration

In Claude Desktop, you should now be able to ask Claude to generate presentations, for example:

> "Create a presentation about sustainable energy solutions with 8 slides in a professional tone"

Claude will use the `generate-presentation` tool and return a link to your new presentation.

## Environment Variables

The server requires the following environment variable:

| Variable | Description | Required |
|----------|-------------|----------|
| `GAMMA_API_KEY` | Your Gamma API key | Yes |

You can set this in:
1. A `.env` file in the `gamma-mcp-server` directory
2. The Claude Desktop configuration (in the `env` section)
3. System environment variables

## Troubleshooting

### Server Won't Start

**Problem**: Error message `GAMMA_API_KEY environment variable is not set`

**Solution**: 
- Verify your `.env` file exists in the `gamma-mcp-server` directory
- Check that the `.env` file contains: `GAMMA_API_KEY=your_actual_key`
- If using Claude Desktop config, verify the `env` section has the correct key

### Module Resolution Errors

**Problem**: `Cannot find module` or `ERR_MODULE_NOT_FOUND` errors

**Solution**:
- Ensure `"type": "module"` is in `package.json`
- Check `tsconfig.json` has `"module": "ES2022"` and `"moduleResolution": "node"`
- Run `npm install` to ensure all dependencies are installed
- Use `--esm` flag with ts-node: `npx ts-node --esm src/index.ts`

### Claude Desktop Can't Find Server

**Problem**: Server doesn't appear in Claude Desktop or fails silently

**Solution**:
- Use absolute paths in `claude_desktop_config.json` (not relative paths like `~/`)
- Verify the path to the server file is correct
- Check Claude Desktop logs:
  - macOS: `~/Library/Logs/Claude/`
  - Windows: `%APPDATA%/Claude/logs/`
- Ensure you completely quit and restarted Claude Desktop after config changes

### API Request Failures

**Problem**: Tool returns errors about API requests

**Solution**:
- Verify your Gamma API key is valid
- Check your internet connection
- Review the error message for specific details
- Ensure the Gamma API service is operational

### Invalid Parameters

**Problem**: Validation errors when calling the tool

**Solution**:
- Ensure `inputText` is provided (it's required)
- Check that enum values match exactly (e.g., `"professional"` not `"Professional"`)
- Verify `numCards` is between 1 and 50 if provided
- Review the parameter documentation above for valid options

### TypeScript Build Errors

**Problem**: Compilation fails with type errors

**Solution**:
- Run `npm install` to ensure all type definitions are installed
- Check `tsconfig.json` settings match the provided configuration
- Verify Node.js version is 18 or higher: `node --version`

## Development

### Type Checking

```bash
npm run typecheck
```

### Project Structure

```
gamma-mcp-server/
├── src/
│   └── index.ts          # Main server implementation
├── dist/                 # Compiled JavaScript (after build)
├── package.json          # Project configuration
├── tsconfig.json         # TypeScript configuration
├── .env                  # Environment variables (not in git)
├── .env.example          # Environment template
└── README.md             # This file
```

## Security Notes

- **Never commit** your `.env` file or expose your API key in code
- The `.env` file is excluded via `.gitignore`
- API keys should only be stored in:
  - Local `.env` files (not tracked by git)
  - Environment variables
  - Secure secrets management systems
- Logs are written to stderr to avoid leaking sensitive data through stdio

## API Reference

For more information about the Gamma API and available options, visit the [Gamma API Documentation](https://gamma.app/docs/api).

## License

MIT

## Support

For issues and questions:
- Check the Troubleshooting section above
- Review Claude Desktop MCP documentation
- Verify Gamma API status and documentation
