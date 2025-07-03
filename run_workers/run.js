import Arcade from "@arcadeai/arcadejs";
import dotenv from "dotenv";

dotenv.config();

const ARCADE_API_KEY = process.env.ARCADE_API_KEY;
const USER_ID = process.env.ARCADE_USER_ID;

const client = new Arcade({
    apiKey: ARCADE_API_KEY,
});

console.log(ARCADE_API_KEY, USER_ID);

const result = await client.tools.execute({
  tool_name: "GetShopifyOrders.GetShopifyOrders@0.1.0",
  input: {
    "owner": "ArcadeAI",
    "name": "arcade-ai",
    "starred": "true",
    "store_key": "OGTHREAD"
  },
  user_id: USER_ID,
})

console.log("Shopify data:", result.output.value);

// Start the authorization process
const authResponse = await client.tools.authorize({
  tool_name: "Google.WriteToCell",
  user_id: USER_ID,
});

if (authResponse.status !== "completed") {
  console.log(`Click this link to authorize: ${authResponse.url}`);
}

// Wait for the authorization to complete
await client.auth.waitForCompletion(authResponse);
console.log("✅ Google Sheets authorization completed");

// Check if we have data to write
if (!result.output.value.summary || result.output.value.summary.length === 0) {
  console.log("❌ No data to write to spreadsheet");
  process.exit(1);
}

// Write headers first
const headers = Object.keys(result.output.value.summary[0]);
console.log("📋 Writing headers:", headers);

const columns = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');

// Write headers to row 1
for (let i = 0; i < headers.length; i++) {
  const toolInput = {
    spreadsheet_id: result.output.value.sheet_id, 
    column: columns[i],
    row: 1,
    value: headers[i],
  };
    
  try {
    console.log(toolInput);
    const response = await client.tools.execute({
      tool_name: "Google.WriteToCell",
      input: toolInput,
      user_id: USER_ID,
    });
    console.log(response);
    if (response.error) {
      console.error(`❌ Error writing header ${headers[i]}:`, response.error);
    } else {
      console.log(`✅ Header ${headers[i]} written successfully`);
    }
  } catch (error) {
    console.error(`❌ Exception writing header ${headers[i]}:`, error);
  }
}

// Write data starting from row 2
let rowIndex = 2;
for (let item of result.output.value.summary) {
    console.log(`📝 Writing row ${rowIndex}...`);
    let colIndex = 0;
    
    for (let [key, val] of Object.entries(item)) {
        const toolInput = {
            spreadsheet_id: "1OlnPiqBUaQXnR83VcacaPA6AJpsrqp1SMNmqf6x8eNc", 
            column: columns[colIndex],
            row: rowIndex,
            value: val.toString(),
        };
        
        try {
          const response = await client.tools.execute({
              tool_name: "Google.WriteToCell",
              input: toolInput,
              user_id: USER_ID,
          });
          console.log(response);
          if (response.error) {
            console.error(`❌ Error writing ${key} to ${columns[colIndex]}${rowIndex}:`, response.error);
          }
        } catch (error) {
          console.error(`❌ Exception writing ${key}:`, error);
        }
        
        colIndex++;
    }
    rowIndex++;
}

console.log("🎉 Data export completed!");

