// MCP Tool definitions and implementations for OmniFlow

export const TOOLS = [
  {
    name: "plan_itinerary",
    description: "Generate an optimized travel or event schedule with daily activities, weather considerations, and estimated budget.",
    inputSchema: {
      type: "object",
      properties: {
        destination: { type: "string", description: "City, park, or venue destination (e.g., Seattle, WA or Olympic National Park)" },
        duration_days: { type: "number", description: "Number of days for the trip" },
        trip_type: { type: "string", enum: ["camping", "urban", "business", "family", "adventure"], description: "Type of trip" },
        budget_limit: { type: "number", description: "Maximum budget in USD" }
      },
      required: ["destination", "duration_days"]
    }
  },
  {
    name: "search_amazon_products",
    description: "Search the Amazon catalog for products matching trip gear, essentials, or user requests with live prices, ratings, and Prime eligibility.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Product search query (e.g. waterproof tent 4 person, hiking boots)" },
        category: { type: "string", description: "Product department (e.g. Sports & Outdoors, Electronics, Apparel)" },
        max_price: { type: "number", description: "Maximum price filter in USD" },
        prime_only: { type: "boolean", description: "Filter by Prime eligible items" }
      },
      required: ["query"]
    }
  },
  {
    name: "optimize_budget_cart",
    description: "Evaluates selected items against target budget, applies bundle discounts, and generates an optimized shopping cart.",
    inputSchema: {
      type: "object",
      properties: {
        items: {
          type: "array",
          items: {
            type: "object",
            properties: {
              asin: { type: "string" },
              title: { type: "string" },
              price: { type: "number" },
              quantity: { type: "number" }
            },
            required: ["asin", "title", "price"]
          }
        },
        budget_limit: { type: "number", description: "Budget limit in USD" }
      },
      required: ["items", "budget_limit"]
    }
  },
  {
    name: "confirm_order_execution",
    description: "Human-in-the-loop checkout trigger. Generates a secured authorization card for one-touch voice/screen confirmation with shipping and payment summary.",
    inputSchema: {
      type: "object",
      properties: {
        cart_id: { type: "string", description: "Identifier for the prepared cart" },
        total_amount: { type: "number", description: "Total price including tax" },
        delivery_address: { type: "string", description: "Shipping address summary" },
        delivery_speed: { type: "string", enum: ["Same-Day Prime", "One-Day Prime", "Two-Day Free"], description: "Selected shipping option" }
      },
      required: ["cart_id", "total_amount"]
    }
  }
];

// Mock catalog for realistic demo data
const PRODUCT_CATALOG = [
  {
    asin: "B09CAMP01",
    title: "Coleman Sundome Camping Tent (4-Person, WeatherTec)",
    price: 89.99,
    original_price: 119.99,
    rating: 4.7,
    reviews_count: 14230,
    prime: true,
    image: "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=500&auto=format&fit=crop&q=60",
    badge: "Overall Pick",
    keywords: ["tent", "camping", "shelter", "outdoor"]
  },
  {
    asin: "B08SLEEP02",
    title: "Oaskys 3-Season Cold Weather Sleeping Bag (Waterproof)",
    price: 36.99,
    original_price: 49.99,
    rating: 4.6,
    reviews_count: 8920,
    prime: true,
    image: "https://images.unsplash.com/photo-1510312305653-8ed496efae75?w=500&auto=format&fit=crop&q=60",
    badge: "Best Seller",
    keywords: ["sleeping bag", "camping", "cold weather", "warmth"]
  },
  {
    asin: "B07LIGHT03",
    title: "Vont 4-Pack LED Camping Lanterns (Super Bright & Collapsible)",
    price: 24.99,
    original_price: 34.99,
    rating: 4.8,
    reviews_count: 22100,
    prime: true,
    image: "https://images.unsplash.com/photo-1517824806704-9040b037703b?w=500&auto=format&fit=crop&q=60",
    badge: "Amazon's Choice",
    keywords: ["lantern", "light", "led", "lamp", "camping"]
  },
  {
    asin: "B09STOVE04",
    title: "Gas One Portable Backpacking Butane Camp Stove with Carry Case",
    price: 29.50,
    original_price: 35.00,
    rating: 4.5,
    reviews_count: 4500,
    prime: true,
    image: "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=500&auto=format&fit=crop&q=60",
    badge: "Great Value",
    keywords: ["stove", "cooking", "camp stove", "gas"]
  },
  {
    asin: "B08PACK05",
    title: "Mountaintop 40L Internal Frame Hiking Backpack",
    price: 52.99,
    original_price: 65.00,
    rating: 4.6,
    reviews_count: 6720,
    prime: true,
    image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&auto=format&fit=crop&q=60",
    badge: "Top Rated",
    keywords: ["backpack", "hiking", "rucksack", "bag"]
  },
  {
    asin: "B0BHYDR06",
    title: "Hydro Flask 32oz Wide Mouth with Flex Cap",
    price: 39.95,
    original_price: 44.95,
    rating: 4.9,
    reviews_count: 31000,
    prime: true,
    image: "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&auto=format&fit=crop&q=60",
    badge: "Amazon's Choice",
    keywords: ["water bottle", "flask", "hydration", "drink"]
  }
];

export async function executeTool(name, args) {
  switch (name) {
    case "plan_itinerary": {
      const { destination, duration_days = 2, trip_type = "adventure", budget_limit = 350 } = args;
      const days = [];
      const activities = [
        { title: `Arrive & Setup Base Camp at ${destination}`, time: "09:00 AM", cost: 35 },
        { title: "Scenic Ridge Trail Exploration & Photography", time: "01:30 PM", cost: 0 },
        { title: "Campfire Dinner & Stargazing Session", time: "07:00 PM", cost: 25 },
        { title: "Sunrise Summit Hike & Flora Trail", time: "06:30 AM", cost: 0 },
        { title: "Lakeside Kayak Rental & Wildlife Observation", time: "11:00 AM", cost: 45 },
        { title: "Departure & Gear Pack-down", time: "04:00 PM", cost: 0 }
      ];

      for (let i = 1; i <= Math.min(duration_days, 5); i++) {
        days.push({
          day: i,
          date: `Day ${i}`,
          theme: i === 1 ? "Arrival & Exploration" : i === duration_days ? "Summit & Farewell" : "Deep Excursion",
          highlights: activities.slice((i - 1) * 2, (i - 1) * 2 + 2),
          weatherForecast: { condition: "Partly Cloudy", high: 68, low: 48, precip: "10%" }
        });
      }

      return {
        destination,
        duration_days,
        trip_type,
        estimated_activities_cost: days.reduce((acc, d) => acc + d.highlights.reduce((sum, h) => sum + h.cost, 0), 0),
        budget_limit,
        itinerary: days,
        recommended_gear: ["4-person tent", "sleeping bag", "camping lantern", "portable stove"]
      };
    }

    case "search_amazon_products": {
      const { query, max_price, prime_only } = args;
      const q = (query || "").toLowerCase();
      let results = PRODUCT_CATALOG.filter(item => {
        const matchesQuery = item.keywords.some(k => q.includes(k)) || item.title.toLowerCase().includes(q);
        const matchesPrice = max_price ? item.price <= max_price : true;
        const matchesPrime = prime_only ? item.prime : true;
        return matchesQuery && matchesPrice && matchesPrime;
      });

      if (results.length === 0) {
        // Fallback to top rated items
        results = PRODUCT_CATALOG.slice(0, 3);
      }

      return {
        query,
        count: results.length,
        products: results
      };
    }

    case "optimize_budget_cart": {
      const { items = [], budget_limit = 250 } = args;
      let runningTotal = 0;
      const optimizedItems = [];

      for (const item of items) {
        const itemTotal = (item.price || 0) * (item.quantity || 1);
        if (runningTotal + itemTotal <= budget_limit + 15) {
          runningTotal += itemTotal;
          optimizedItems.push({
            ...item,
            quantity: item.quantity || 1,
            subtotal: parseFloat(itemTotal.toFixed(2))
          });
        }
      }

      const bundleDiscount = optimizedItems.length >= 3 ? 12.50 : 0;
      const estimatedTax = parseFloat(((runningTotal - bundleDiscount) * 0.0825).toFixed(2));
      const finalTotal = parseFloat((runningTotal - bundleDiscount + estimatedTax).toFixed(2));

      return {
        cart_id: "CART_" + Math.random().toString(36).substring(2, 9).toUpperCase(),
        original_subtotal: parseFloat(runningTotal.toFixed(2)),
        bundle_discount: bundleDiscount,
        estimated_tax: estimatedTax,
        final_total: finalTotal,
        budget_limit,
        within_budget: finalTotal <= budget_limit,
        items: optimizedItems
      };
    }

    case "confirm_order_execution": {
      const { cart_id, total_amount, delivery_address = "410 Terry Ave N, Seattle, WA", delivery_speed = "One-Day Prime" } = args;
      const order_id = "AMZ-702-" + Math.floor(1000000 + Math.random() * 9000000);
      return {
        status: "CONFIRMED_PREPARED",
        order_id,
        cart_id,
        total_amount,
        delivery_address,
        delivery_speed,
        estimated_arrival: "Tomorrow by 2:00 PM",
        one_click_trigger_token: "TOKEN_" + Buffer.from(order_id).toString("base64"),
        security_guardrail_applied: true
      };
    }

    default:
      throw new Error(`Tool ${name} not found`);
  }
}
