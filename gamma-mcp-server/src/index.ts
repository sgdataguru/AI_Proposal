#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";
import fetch from "node-fetch";
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

// Validate API key is present
const GAMMA_API_KEY = process.env.GAMMA_API_KEY;
if (!GAMMA_API_KEY) {
  console.error("ERROR: GAMMA_API_KEY environment variable is not set.");
  console.error("Please add your Gamma API key to the .env file.");
  process.exit(1);
}

// Gamma API endpoint
const GAMMA_API_URL = "https://api.gamma.app/api/v1/generate";

// Zod schema for tool parameters
const GeneratePresentationSchema = z.object({
  inputText: z.string().min(1, "Input text is required"),
  tone: z.enum(["professional", "casual", "enthusiastic", "informative"]).optional(),
  audience: z.string().optional(),
  textAmount: z.enum(["concise", "balanced", "detailed"]).optional(),
  textMode: z.enum(["auto", "cards", "bullets", "paragraphs"]).optional(),
  numCards: z.number().int().positive().max(50).optional(),
  imageModel: z.enum(["dalle2", "dalle3", "sdxl"]).optional(),
  imageStyle: z.enum(["photographic", "digital_art", "illustration", "3d_render"]).optional(),
  editorMode: z.enum(["present", "card", "doc"]).optional(),
  additionalInstructions: z.string().optional(),
});

type GeneratePresentationParams = z.infer<typeof GeneratePresentationSchema>;

/**
 * Generates a presentation using the Gamma API
 */
async function generatePresentation(
  params: GeneratePresentationParams
): Promise<string> {
  try {
    const response = await fetch(GAMMA_API_URL, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${GAMMA_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: params.inputText,
        tone: params.tone,
        audience: params.audience,
        text_amount: params.textAmount,
        text_mode: params.textMode,
        num_cards: params.numCards,
        image_model: params.imageModel,
        image_style: params.imageStyle,
        editor_mode: params.editorMode,
        additional_instructions: params.additionalInstructions,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `Gamma API request failed with status ${response.status}: ${errorText}`
      );
    }

    const data = await response.json() as { url?: string; link?: string; presentation_url?: string };
    
    // Handle different possible response formats
    const presentationUrl = data.url || data.link || data.presentation_url;
    
    if (!presentationUrl) {
      throw new Error("No presentation URL returned from Gamma API");
    }

    return presentationUrl;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to generate presentation: ${error.message}`);
    }
    throw new Error("Failed to generate presentation: Unknown error");
  }
}

// Initialize MCP server
const server = new Server(
  {
    name: "gamma-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Register tool handlers
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "generate-presentation",
        description:
          "Generate a presentation using Gamma API. Provide input text and optional parameters to customize the presentation.",
        inputSchema: {
          type: "object",
          properties: {
            inputText: {
              type: "string",
              description: "The main content/prompt for the presentation (required)",
            },
            tone: {
              type: "string",
              enum: ["professional", "casual", "enthusiastic", "informative"],
              description: "The tone of the presentation",
            },
            audience: {
              type: "string",
              description: "Target audience for the presentation",
            },
            textAmount: {
              type: "string",
              enum: ["concise", "balanced", "detailed"],
              description: "Amount of text per slide",
            },
            textMode: {
              type: "string",
              enum: ["auto", "cards", "bullets", "paragraphs"],
              description: "How text should be formatted",
            },
            numCards: {
              type: "number",
              description: "Number of slides (1-50)",
              minimum: 1,
              maximum: 50,
            },
            imageModel: {
              type: "string",
              enum: ["dalle2", "dalle3", "sdxl"],
              description: "AI model for generating images",
            },
            imageStyle: {
              type: "string",
              enum: ["photographic", "digital_art", "illustration", "3d_render"],
              description: "Style of generated images",
            },
            editorMode: {
              type: "string",
              enum: ["present", "card", "doc"],
              description: "Editor mode for the presentation",
            },
            additionalInstructions: {
              type: "string",
              description: "Additional instructions for presentation generation",
            },
          },
          required: ["inputText"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "generate-presentation") {
    try {
      // Validate parameters
      const params = GeneratePresentationSchema.parse(request.params.arguments);

      // Generate presentation
      const presentationUrl = await generatePresentation(params);

      return {
        content: [
          {
            type: "text",
            text: `Successfully generated presentation! View it here: ${presentationUrl}`,
          },
        ],
      };
    } catch (error) {
      if (error instanceof z.ZodError) {
        const errorMessages = error.errors
          .map((err) => `${err.path.join(".")}: ${err.message}`)
          .join(", ");
        return {
          content: [
            {
              type: "text",
              text: `Validation error: ${errorMessages}`,
            },
          ],
          isError: true,
        };
      }

      if (error instanceof Error) {
        return {
          content: [
            {
              type: "text",
              text: `Error: ${error.message}`,
            },
          ],
          isError: true,
        };
      }

      return {
        content: [
          {
            type: "text",
            text: "An unknown error occurred while generating the presentation.",
          },
        ],
        isError: true,
      };
    }
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Gamma MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
