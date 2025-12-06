#!/usr/bin/env node

/**
 * Test the EXACT payload from the GitHub issue
 */

import { z } from "zod";

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

// EXACT payload from the issue
const issuePayload = {
  "inputText": "AI Lead Scoring & Activation for wealth management in India: a 5-week PoC roadmap",
  "tone": "professional and crisp",
  "audience": "wealth RMs and business stakeholders",
  "textAmount": "medium",
  "textMode": "generate",
  "numCards": 12,
  "imageModel": "auto",
  "imageStyle": "clean corporate",
  "editorMode": "auto",
  "additionalInstructions": "Include a simple architecture slide, a 5-week timeline, and a governance-by-design checklist."
};

console.log("Testing EXACT payload from issue...\n");

try {
  const result = GeneratePresentationSchema.parse(issuePayload);
  console.log("✅ Payload validated successfully");
  console.log(JSON.stringify(result, null, 2));
} catch (error) {
  if (error instanceof z.ZodError) {
    console.log("❌ Validation failed with errors:");
    error.errors.forEach((err) => {
      console.log(`  - ${err.path.join(".")}: ${err.message}`);
      if (err.code === 'invalid_enum_value') {
        console.log(`    Received: "${err.received}"`);
        console.log(`    Expected: ${JSON.stringify(err.options)}`);
      }
    });
  } else {
    console.log("❌ Unexpected error:", error);
  }
}
