import { TOOLS, executeTool } from "../src/tools.js";
import { runAgentWorkflow } from "../src/bedrockAgent.js";

async function runTests() {
  console.log("🧪 Starting OmniFlow MCP & Agent Verification Tests...\n");

  // 1. Verify Tools definition
  console.log("1️⃣ Checking MCP Tools definitions...");
  if (TOOLS.length !== 4) {
    throw new Error(`Expected 4 tools, got ${TOOLS.length}`);
  }
  console.log(`✅ Loaded ${TOOLS.length} MCP Tools with JSONSchema specifications:`);
  TOOLS.forEach(t => console.log(`   - ${t.name}: ${t.description.substring(0, 60)}...`));

  // 2. Test Tool Execution: plan_itinerary
  console.log("\n2️⃣ Testing Tool Execution: plan_itinerary...");
  const itinerary = await executeTool("plan_itinerary", {
    destination: "Mount Rainier",
    duration_days: 2,
    budget_limit: 250
  });
  if (!itinerary.itinerary || itinerary.itinerary.length !== 2) {
    throw new Error("Failed to generate correct itinerary days");
  }
  console.log(`✅ Itinerary planned for ${itinerary.destination} (${itinerary.duration_days} days, estimated cost: $${itinerary.estimated_activities_cost})`);

  // 3. Test Tool Execution: search_amazon_products
  console.log("\n3️⃣ Testing Tool Execution: search_amazon_products...");
  const search = await executeTool("search_amazon_products", {
    query: "camping tent",
    prime_only: true
  });
  if (!search.products || search.products.length === 0) {
    throw new Error("Failed product search");
  }
  console.log(`✅ Found ${search.products.length} products. First match: "${search.products[0].title}" ($${search.products[0].price})`);

  // 4. Test Tool Execution: optimize_budget_cart
  console.log("\n4️⃣ Testing Tool Execution: optimize_budget_cart...");
  const cart = await executeTool("optimize_budget_cart", {
    items: [
      { asin: "B09CAMP01", title: "Coleman Tent", price: 89.99, quantity: 1 },
      { asin: "B07LIGHT03", title: "Vont Lantern", price: 24.99, quantity: 1 }
    ],
    budget_limit: 200
  });
  console.log(`✅ Cart generated (${cart.cart_id}): Total $${cart.final_total} (Within budget: ${cart.within_budget})`);

  // 5. Test Full Agent Workflow & Visual Cards
  console.log("\n5️⃣ Testing Full Autonomous Agent Workflow...");
  const workflow = await runAgentWorkflow("Plan a weekend camping trip to Olympic National Park under $300 and order gear");
  console.log(`✅ Spoken Response generated (${workflow.spokenResponse.length} chars)`);
  console.log(`✅ Agent executed ${workflow.steps.length} reasoning & tool steps`);
  console.log(`✅ Generated ${workflow.cards.length} Multi-Modal Visual Cards:`);
  workflow.cards.forEach(c => console.log(`   - Card [${c.type}]: ${c.title}`));

  console.log("\n🎉 ALL TESTS PASSED SUCCESSFULLY! Ready for Hackathon Submission.");
}

runTests().catch(err => {
  console.error("❌ Test failed:", err);
  process.exit(1);
});
