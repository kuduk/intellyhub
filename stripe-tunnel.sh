#!/bin/bash

# Script per avviare il tunnel Stripe per testing locale
# Questo script avvia il listener Stripe che inoltra i webhook al server locale

echo "🚀 Avvio tunnel Stripe per testing locale..."
echo ""
echo "Questo script:"
echo "- Avvia stripe listen per intercettare i webhook"
echo "- Inoltra gli eventi al webhook endpoint locale"
echo "- Fornisce un STRIPE_WEBHOOK_SECRET temporaneo"
echo ""
echo "💡 Ricordati di:"
echo "1. Aver fatto 'stripe login' almeno una volta"
echo "2. Copiare il STRIPE_WEBHOOK_SECRET nel file .env"
echo "3. Avere il server locale in esecuzione su porta 5000"
echo ""
echo "📍 Webhook endpoint: http://localhost:5000/api/billing/webhook"
echo ""

# Controlla se Stripe CLI è installato
if ! command -v stripe &> /dev/null; then
    echo "❌ Errore: Stripe CLI non trovato!"
    echo "Installa Stripe CLI: https://stripe.com/docs/stripe-cli"
    exit 1
fi

echo "✅ Stripe CLI trovato, avvio tunnel..."
echo ""

# Avvia il tunnel
stripe listen --forward-to localhost:5000/api/billing/webhook