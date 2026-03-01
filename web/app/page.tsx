"use client";
import { useSession } from "@livekit/components-react";
import { TokenSource, ConnectionState } from "livekit-client";
import { AgentSessionProvider } from "@/components/agents-ui/agent-session-provider";
import { AgentUI } from "@/components/agent-ui";

const TOKEN_SOURCE = TokenSource.endpoint("/api/v1/token");

export default function HomePage() {
  const session = useSession(TOKEN_SOURCE, {
    agentName: "customer-support-assistant",
  });

  const isActive = session.connectionState !== ConnectionState.Disconnected;

  return (
    <main className="min-h-screen bg-background flex items-center justify-center">
      <AgentSessionProvider session={session}>
        <AgentUI
          isActive={isActive}
          isConnected={session.isConnected}
          onStart={() => session.start()}
        />
      </AgentSessionProvider>
    </main>
  );
}
