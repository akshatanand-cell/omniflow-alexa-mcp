import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { TOOLS, executeTool } from "./tools.js";
import { runAgentWorkflow } from "./bedrockAgent.js";

import path from "path";
import { fileURLToPath } from "url";

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "../public")));

// Standard MCP Specification Version 2025-11-25
const MCP_PROTOCOL_VERSION = "2025-11-25";

// Health / Info endpoint
app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    service: "OmniFlow Alexa+ MCP Server",
    protocolVersion: MCP_PROTOCOL_VERSION,
    timestamp: new Date().toISOString()
  });
});

// MCP Discovery endpoint
app.get("/mcp/info", (req, res) => {
  res.json({
    name: "omniflow-alexa-mcp",
    version: "1.0.0",
    protocolVersion: MCP_PROTOCOL_VERSION,
    capabilities: {
      tools: { listChanged: true },
      resources: { subscribe: true },
      prompts: { listChanged: false },
      logging: {}
    },
    transport: "streamable-http",
    toolsCount: TOOLS.length
  });
});

// Standard MCP JSON-RPC 2.0 Handler
app.post("/mcp", async (req, res) => {
  const { jsonrpc, id, method, params } = req.body;

  if (jsonrpc !== "2.0") {
    return res.status(400).json({
      jsonrpc: "2.0",
      id: id || null,
      error: { code: -32600, message: "Invalid Request: jsonrpc must be 2.0" }
    });
  }

  try {
    switch (method) {
      case "initialize":
        return res.json({
          jsonrpc: "2.0",
          id,
          result: {
            protocolVersion: MCP_PROTOCOL_VERSION,
            serverInfo: {
              name: "omniflow-alexa-mcp",
              version: "1.0.0"
            },
            capabilities: {
              tools: {},
              resources: {},
              prompts: {}
            }
          }
        });

      case "tools/list":
        return res.json({
          jsonrpc: "2.0",
          id,
          result: {
            tools: TOOLS
          }
        });

      case "tools/call": {
        const { name, arguments: toolArgs } = params || {};
        if (!name) {
          return res.status(400).json({
            jsonrpc: "2.0",
            id,
            error: { code: -32602, message: "Missing tool name in params" }
          });
        }

        const toolResult = await executeTool(name, toolArgs || {});
        return res.json({
          jsonrpc: "2.0",
          id,
          result: {
            content: [
              {
                type: "text",
                text: JSON.stringify(toolResult, null, 2)
              }
            ],
            isError: false
          }
        });
      }

      default:
        return res.status(404).json({
          jsonrpc: "2.0",
          id,
          error: { code: -32601, message: `Method '${method}' not found` }
        });
    }
  } catch (err) {
    return res.status(500).json({
      jsonrpc: "2.0",
      id,
      error: { code: -32000, message: err.message }
    });
  }
});

// Streamable HTTP / Server-Sent Events (SSE) Transport endpoint
app.get("/mcp/stream", (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
  res.flushHeaders();

  res.write(`data: ${JSON.stringify({ type: "connection", message: "Connected to OmniFlow Streamable HTTP MCP Stream", protocolVersion: MCP_PROTOCOL_VERSION })}\n\n`);

  const keepAlive = setInterval(() => {
    res.write(`data: ${JSON.stringify({ type: "heartbeat", timestamp: Date.now() })}\n\n`);
  }, 15000);

  req.on("close", () => {
    clearInterval(keepAlive);
  });
});

// Alexa+ Autonomous Web Agent interaction endpoint
app.post("/api/agent/chat", async (req, res) => {
  try {
    const { message, history } = req.body;
    if (!message) {
      return res.status(400).json({ error: "Message is required" });
    }

    const response = await runAgentWorkflow(message, history || []);
    res.json(response);
  } catch (err) {
    console.error("Agent error:", err);
    res.status(500).json({ error: err.message });
  }
});

// Quick action: finalize order
app.post("/api/agent/confirm-order", async (req, res) => {
  const { cart_id, total } = req.body;
  const result = await executeTool("confirm_order_execution", {
    cart_id: cart_id || "CART_CONFIRMED",
    total_amount: total || 163.97
  });
  res.json({
    success: true,
    result,
    message: `Order #${result.order_id} successfully confirmed with 1-Day Prime delivery!`
  });
});

app.listen(PORT, () => {
  console.log(`====================================================`);
  console.log(`🚀 OmniFlow Alexa+ MCP Server running on port ${PORT}`);
  console.log(`📡 MCP Protocol: ${MCP_PROTOCOL_VERSION} (Streamable HTTP)`);
  console.log(`🔗 MCP Info: http://localhost:${PORT}/mcp/info`);
  console.log(`⚡ JSON-RPC: http://localhost:${PORT}/mcp`);
  console.log(`====================================================`);
});
