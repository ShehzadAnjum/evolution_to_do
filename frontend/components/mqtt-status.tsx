"use client";

import { useState, useEffect, useCallback } from "react";
import { Button } from "@/components/ui/button";

interface MqttHealth {
  mqtt_connected: boolean;
  device_online: boolean;
  last_heartbeat: string | null;
  wifi_rssi: number | null;
}

interface MqttStatusProps {
  token: string;
}

export function MqttStatus({ token }: MqttStatusProps) {
  const [health, setHealth] = useState<MqttHealth | null>(null);
  const [loading, setLoading] = useState(true);
  const [reconnecting, setReconnecting] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const fetchHealth = useCallback(async (showRefreshing = false) => {
    if (showRefreshing) setRefreshing(true);
    try {
      // Start fetch and minimum delay in parallel
      const [res] = await Promise.all([
        fetch(`${API_URL}/api/devices/health`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          cache: "no-store",
        }),
        // Minimum 500ms delay when manually refreshing so spinner is visible
        showRefreshing ? new Promise(r => setTimeout(r, 500)) : Promise.resolve(),
      ]);
      if (res.ok) {
        const data = await res.json();
        setHealth(data);
        setError(null);
      } else {
        setError("Failed to fetch status");
      }
    } catch (err) {
      setError("Connection error");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [token, API_URL]);

  const reconnect = async () => {
    setReconnecting(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}/api/devices/reconnect`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await res.json();
      if (data.success) {
        await fetchHealth(true);
      } else {
        setError(data.message || "Reconnection failed");
      }
    } catch (err) {
      setError("Reconnection error");
    } finally {
      setReconnecting(false);
    }
  };

  useEffect(() => {
    fetchHealth(false);
    // Poll every 15 seconds (matches ESP32 heartbeat timeout)
    const interval = setInterval(() => fetchHealth(false), 15000);
    return () => clearInterval(interval);
  }, [fetchHealth]);

  if (loading) {
    return (
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <div className="w-2 h-2 rounded-full bg-gray-400 animate-pulse" />
        <span>Checking MQTT...</span>
      </div>
    );
  }

  const mqttConnected = health?.mqtt_connected ?? false;
  const deviceOnline = health?.device_online ?? false;

  return (
    <div className="flex items-center gap-3 p-2 rounded-lg border bg-card">
      {/* MQTT Status */}
      <div className="flex items-center gap-2">
        <div
          className={`w-2.5 h-2.5 rounded-full ${
            mqttConnected ? "bg-green-500" : "bg-red-500 animate-pulse"
          }`}
        />
        <span className="text-sm font-medium">
          MQTT: {mqttConnected ? "Connected" : "Disconnected"}
        </span>
      </div>

      {/* Device Status */}
      <div className={`flex items-center gap-2 ${deviceOnline ? "text-foreground" : "text-muted-foreground"}`}>
        <div
          className={`w-2 h-2 rounded-full ${
            deviceOnline ? "bg-blue-500" : "bg-gray-400"
          }`}
        />
        <span className={`text-xs ${deviceOnline ? "font-medium" : ""}`}>
          ESP32: {deviceOnline ? "Online" : "Offline"}
        </span>
        {/* WiFi Signal - only show when online */}
        {deviceOnline && health?.wifi_rssi && (
          <span className="text-xs">
            {health.wifi_rssi}dBm
          </span>
        )}
      </div>

      {/* Reconnect Button (only shown when disconnected) */}
      {!mqttConnected && (
        <Button
          size="sm"
          variant="outline"
          onClick={reconnect}
          disabled={reconnecting}
          className="h-7 px-2 text-xs"
        >
          {reconnecting ? "Reconnecting..." : "Reconnect"}
        </Button>
      )}

      {/* Refresh Button */}
      <Button
        size="sm"
        variant="ghost"
        onClick={() => fetchHealth(true)}
        disabled={refreshing}
        className="h-7 w-7 p-0"
        title="Refresh status"
      >
        {refreshing ? (
          /* Spinning loader when refreshing */
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            className="animate-spin"
          >
            <path d="M21 12a9 9 0 1 1-6.219-8.56" />
          </svg>
        ) : (
          /* Refresh icon when idle */
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M21 2v6h-6" />
            <path d="M3 12a9 9 0 0 1 15-6.7L21 8" />
            <path d="M3 22v-6h6" />
            <path d="M21 12a9 9 0 0 1-15 6.7L3 16" />
          </svg>
        )}
      </Button>

      {/* Error */}
      {error && <span className="text-xs text-red-500">{error}</span>}
    </div>
  );
}
