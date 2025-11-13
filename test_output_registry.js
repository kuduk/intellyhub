// Test rapido per verificare che il sistema funzioni
// Questo simula il comportamento del frontend

// Simulazione dei dati di flow
const testFlowData = {
  states: {
    // Listener legacy (senza output) - dovrebbe generare variabili individuali
    telegram_listener_legacy: {
      state_type: "telegram-listener",
      bot_token: "test_token"
      // Nessun parametro 'output' -> comportamento legacy
    },
    
    // Listener strutturato (con output) - dovrebbe generare una variabile strutturata
    telegram_listener_structured: {
      state_type: "telegram-listener", 
      bot_token: "test_token",
      output: "telegram_data"  // <- Con output
    },
    
    // Webhook listener senza output
    webhook_legacy: {
      state_type: "webhook-listener",
      port: 8080
      // Nessun output -> variabili legacy
    },
    
    // Stato normale con output (dovrebbe funzionare come prima)
    llm_state: {
      state_type: "llm_agent",
      provider: "openai",
      model: "gpt-4",
      output: "ai_response"
    }
  }
}

// Risultati attesi:
console.log("=== RISULTATI ATTESI ===")
console.log("telegram_listener_legacy dovrebbe generare:")
console.log("- telegram_message_text (legacy)")
console.log("- telegram_chat_id (legacy)")
console.log("- telegram_user_id (legacy)")
console.log("- ... altre variabili individuali")
console.log("")
console.log("telegram_listener_structured dovrebbe generare:")
console.log("- telegram_data (strutturato)")
console.log("")
console.log("webhook_legacy dovrebbe generare:")
console.log("- webhook_data (legacy)")
console.log("- webhook_headers (legacy)")
console.log("- webhook_method (legacy)")
console.log("- webhook_ip (legacy)")
console.log("")
console.log("llm_state dovrebbe generare:")
console.log("- ai_response (normale)")

console.log("\n=== FRONTEND DOVREBBE MOSTRARE ===")
console.log("Nel pannello variabili:")
console.log("• telegram_message_text [string] Legacy 🕐")
console.log("• telegram_chat_id [string] Legacy 🕐") 
console.log("• telegram_data [object] 📦")
console.log("• webhook_data [object] Legacy 🕐")
console.log("• ai_response [object] 📦")