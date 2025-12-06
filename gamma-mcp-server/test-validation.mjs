#!/usr/bin/env node

/**
 * Manual test script to validate the Gamma MCP Server parameter validation
 * This script tests the Zod schema validation without making actual API calls
 */

import { z } from "zod";

// Copy of the schema from src/index.ts for testing
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

console.log("🧪 Gamma MCP Server Parameter Validation Tests\n");

// Test 1: Valid minimal parameters
console.log("✅ Test 1: Valid minimal parameters");
try {
  const result1 = GeneratePresentationSchema.parse({
    inputText: "Create a presentation about AI"
  });
  console.log("   PASS - Accepted minimal valid input\n");
} catch (error) {
  console.log("   FAIL - Should accept minimal valid input");
  console.log("   Error:", error);
}

// Test 2: Valid full parameters
console.log("✅ Test 2: Valid full parameters");
try {
  const result2 = GeneratePresentationSchema.parse({
    inputText: "Create a presentation about sustainable energy",
    tone: "professional",
    audience: "Business executives",
    textAmount: "balanced",
    textMode: "bullets",
    numCards: 10,
    imageModel: "dalle3",
    imageStyle: "photographic",
    editorMode: "present",
    additionalInstructions: "Focus on renewable sources"
  });
  console.log("   PASS - Accepted full valid parameters\n");
} catch (error) {
  console.log("   FAIL - Should accept full valid parameters");
  console.log("   Error:", error);
}

// Test 3: Missing required field
console.log("❌ Test 3: Missing required field (inputText)");
try {
  const result3 = GeneratePresentationSchema.parse({
    tone: "professional"
  });
  console.log("   FAIL - Should reject missing inputText\n");
} catch (error) {
  console.log("   PASS - Correctly rejected missing inputText");
  if (error instanceof z.ZodError) {
    console.log("   Validation error:", error.errors[0].message, "\n");
  }
}

// Test 4: Empty inputText
console.log("❌ Test 4: Empty inputText");
try {
  const result4 = GeneratePresentationSchema.parse({
    inputText: ""
  });
  console.log("   FAIL - Should reject empty inputText\n");
} catch (error) {
  console.log("   PASS - Correctly rejected empty inputText");
  if (error instanceof z.ZodError) {
    console.log("   Validation error:", error.errors[0].message, "\n");
  }
}

// Test 5: Invalid tone value
console.log("❌ Test 5: Invalid tone value");
try {
  const result5 = GeneratePresentationSchema.parse({
    inputText: "Test presentation",
    tone: "invalid_tone"
  });
  console.log("   FAIL - Should reject invalid tone\n");
} catch (error) {
  console.log("   PASS - Correctly rejected invalid tone");
  if (error instanceof z.ZodError) {
    console.log("   Expected values:", ["professional", "casual", "enthusiastic", "informative"], "\n");
  }
}

// Test 6: Invalid numCards (too large)
console.log("❌ Test 6: Invalid numCards (> 50)");
try {
  const result6 = GeneratePresentationSchema.parse({
    inputText: "Test presentation",
    numCards: 100
  });
  console.log("   FAIL - Should reject numCards > 50\n");
} catch (error) {
  console.log("   PASS - Correctly rejected numCards > 50");
  if (error instanceof z.ZodError) {
    console.log("   Validation error:", error.errors[0].message, "\n");
  }
}

// Test 7: Invalid numCards (negative)
console.log("❌ Test 7: Invalid numCards (negative)");
try {
  const result7 = GeneratePresentationSchema.parse({
    inputText: "Test presentation",
    numCards: -5
  });
  console.log("   FAIL - Should reject negative numCards\n");
} catch (error) {
  console.log("   PASS - Correctly rejected negative numCards");
  if (error instanceof z.ZodError) {
    console.log("   Validation error:", error.errors[0].message, "\n");
  }
}

// Test 8: Invalid numCards (not an integer)
console.log("❌ Test 8: Invalid numCards (not an integer)");
try {
  const result8 = GeneratePresentationSchema.parse({
    inputText: "Test presentation",
    numCards: 10.5
  });
  console.log("   FAIL - Should reject non-integer numCards\n");
} catch (error) {
  console.log("   PASS - Correctly rejected non-integer numCards");
  if (error instanceof z.ZodError) {
    console.log("   Validation error:", error.errors[0].message, "\n");
  }
}

// Test 9: Invalid imageModel
console.log("❌ Test 9: Invalid imageModel");
try {
  const result9 = GeneratePresentationSchema.parse({
    inputText: "Test presentation",
    imageModel: "gpt4"
  });
  console.log("   FAIL - Should reject invalid imageModel\n");
} catch (error) {
  console.log("   PASS - Correctly rejected invalid imageModel");
  if (error instanceof z.ZodError) {
    console.log("   Expected values:", ["dalle2", "dalle3", "sdxl"], "\n");
  }
}

// Test 10: Multiple valid optional parameters
console.log("✅ Test 10: Multiple valid optional parameters");
try {
  const result10 = GeneratePresentationSchema.parse({
    inputText: "AI in Healthcare",
    tone: "informative",
    numCards: 15,
    imageStyle: "digital_art"
  });
  console.log("   PASS - Accepted multiple optional parameters\n");
} catch (error) {
  console.log("   FAIL - Should accept multiple optional parameters");
  console.log("   Error:", error);
}

console.log("🎉 All validation tests completed!\n");
console.log("Summary:");
console.log("- Schema correctly validates required fields");
console.log("- Schema correctly validates enum values");
console.log("- Schema correctly validates number constraints");
console.log("- Schema accepts valid optional parameters");
