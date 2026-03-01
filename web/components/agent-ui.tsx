"use client";
import {
  useVoiceAssistant,
  useSessionContext,
  useSessionMessages,
  useAgent,
} from "@livekit/components-react";
import { AgentControlBar } from "./agents-ui/agent-control-bar";
import { AgentAudioVisualizerBar } from "./agents-ui/agent-audio-visualizer-bar";
import { AgentChatTranscript } from "./agents-ui/agent-chat-transcript";
import { PhoneCallIcon } from "lucide-react";
import { Button } from "./ui/button";

export const AgentUI = ({
  isActive,
  isConnected,
  onStart,
}: {
  isActive: boolean;
  isConnected: boolean;
  onStart: () => void;
}) => {
  const { audioTrack, state } = useVoiceAssistant();
  const { state: agentState } = useAgent();
  const session = useSessionContext();
  const { messages } = useSessionMessages(session);

  if (!isActive) {
    return (
      <div className="flex flex-col items-center gap-4">
        <Button size="lg" className="rounded-full w-20 h-20" onClick={onStart}>
          <PhoneCallIcon className="w-8 h-8" />
        </Button>
        <p className="text-sm text-muted-foreground">Tap to call support</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center gap-6 w-full max-w-md h-screen py-10">
      <AgentAudioVisualizerBar
        size="xl"
        barCount={5}
        state={state}
        audioTrack={audioTrack}
      />
      <AgentChatTranscript
        agentState={agentState}
        messages={messages}
        className="w-full flex-1 overflow-y-auto min-h-0"
      />
      <AgentControlBar
        variant="livekit"
        isChatOpen={false}
        isConnected={isConnected}
        controls={{
          leave: true,
          microphone: true,
          screenShare: false,
          camera: false,
          chat: false,
        }}
      />
    </div>
  );
};
