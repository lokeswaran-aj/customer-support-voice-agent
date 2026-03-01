"use client";
import {
  useVoiceAssistant,
  useAgent,
  useSessionContext,
  useSessionMessages,
} from "@livekit/components-react";
import { AgentControlBar } from "./agents-ui/agent-control-bar";
import { AgentAudioVisualizerBar } from "./agents-ui/agent-audio-visualizer-bar";
import { AgentChatTranscript } from "./agents-ui/agent-chat-transcript";

export const AgentUI = () => {
  const { audioTrack, state } = useVoiceAssistant();
  const { state: agentState } = useAgent();
  const session = useSessionContext();
  const { messages } = useSessionMessages(session);

  const { room } = session;
  const isConnected = session.isConnected;
  const info = isConnected
    ? [
        { label: "Room Name", value: room.name },
        {
          label: "Participant Identity",
          value: room.localParticipant.identity,
        },
        { label: "Participant Name", value: room.localParticipant.name ?? "—" },
      ]
    : [];

  return (
    <div className="h-full flex flex-col items-center gap-6 max-w-md mx-auto px-6 py-10">
      {isConnected && (
        <div className="w-full rounded-lg border bg-muted/40 px-4 py-3 text-xs text-muted-foreground space-y-1">
          {info.map(({ label, value }) => (
            <div key={label} className="flex justify-between gap-4">
              <span className="font-medium">{label}</span>
              <span className="font-mono truncate">{value}</span>
            </div>
          ))}
        </div>
      )}
      <AgentAudioVisualizerBar
        size="xl"
        barCount={5}
        state={state}
        audioTrack={audioTrack}
      />
      <AgentChatTranscript
        agentState={agentState}
        messages={messages}
        className="w-full min-h-0"
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
