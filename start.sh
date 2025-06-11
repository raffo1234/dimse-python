#!/bin/bash

echo "🔒 Starting tailscaled (userspace)..."
tailscaled --tun=userspace-networking --socks5-server=localhost:1055 &
sleep 5

echo "🔑 Logging in to Tailscale..."
tailscale up --authkey=${TAILSCALE_AUTHKEY} --hostname=render-dicom

echo "✅ Tailscale connected!"
tailscale status

echo "🚀 Starting Flask server..."
exec python main.py
