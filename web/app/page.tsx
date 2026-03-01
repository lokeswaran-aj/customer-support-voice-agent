"use client";
import { useSession } from "@livekit/components-react";
import { TokenSource, ConnectionState } from "livekit-client";
import { AgentSessionProvider } from "@/components/agents-ui/agent-session-provider";
import { AgentUI } from "@/components/agent-ui";
import { PhoneCallIcon } from "lucide-react";
import { Button } from "@/components/ui/button";

const TOKEN_SOURCE = TokenSource.endpoint("/api/v1/token");

export default function HomePage() {
  const session = useSession(TOKEN_SOURCE, {
    agentName: "customer-support-assistant",
  });

  const isActive = session.connectionState !== ConnectionState.Disconnected;

  return (
    <main className="h-screen bg-background overflow-hidden">
      <AgentSessionProvider session={session}>
        {isActive ? (
          <AgentUI />
        ) : (
          <div className="h-full flex flex-col items-center justify-center gap-4">
            <Button
              size="lg"
              className="rounded-full w-20 h-20"
              onClick={() => session.start()}
            >
              <PhoneCallIcon className="w-8 h-8" />
            </Button>
            <p className="text-sm text-muted-foreground">Tap to call support</p>
          </div>
        )}
      </AgentSessionProvider>
    </main>
  );
}
