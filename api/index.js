import express from "express";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";
import { TOOLS, executeTool } from "../server/src/tools.js";
import { runAgentWorkflow } from "../server/src/bedrockAgent.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const MCP_PROTOCOL_VERSION = "2025-11-25";

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "../server/public")));

app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    service: "OmniFlow Alexa+ MCP Server",
    protocolVersion: MCP_PROTOCOL_VERSION,
    timestamp: new Date().toISOString()
  });
});

app.get("/mcp/info", (req, res) => {
  res.json({
    name: "omniflow-alexa-mcp",
    version: "1.0.0",
    protocolVersion: MCP_PROTOCOL_VERSION,
    capabilities: {
      tools: { listChanged: true },
      resources: { subscribe: true },
      prompts: { listChanged: false }
    },
    transport: "streamable-http",
    toolsCount: TOOLS.length
  });
});

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
            serverInfo: { name: "omniflow-alexa-mcp", version: "1.0.0" },
            capabilities: { tools: {}, resources: {}, prompts: {} }
          }
        });

      case "tools/list":
        return res.json({ jsonrpc: "2.0", id, result: { tools: TOOLS } });

      case "tools/call": {
        const { name, arguments: toolArgs } = params || {};
        const toolResult = await executeTool(name, toolArgs || {});
        return res.json({
          jsonrpc: "2.0",
          id,
          result: {
            content: [{ type: "text", text: JSON.stringify(toolResult, null, 2) }],
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
    return res.status(500).json({ jsonrpc: "2.0", id, error: { code: -32000, message: err.message } });
  }
});

app.post("/api/agent/chat", async (req, res) => {
  try {
    const { message, history } = req.body;
    const response = await runAgentWorkflow(message, history || []);
    res.json(response);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

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

export default app;
