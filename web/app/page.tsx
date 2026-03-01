"use client";
import { Button } from "@/components/ui/button";
import { PhoneCallIcon, BikeIcon } from "lucide-react";
import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-background flex flex-col">
      {/* Hero */}
      <section className="flex-1 flex flex-col items-center justify-center text-center px-6 gap-5">
        <div className="w-14 h-14 rounded-2xl bg-primary flex items-center justify-center mb-2">
          <BikeIcon className="w-7 h-7 text-primary-foreground" />
        </div>

        <div>
          <p className="text-xs font-medium uppercase tracking-widest text-muted-foreground mb-3">
            Quickbite &mdash; Voice AI
          </p>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight">
            Customer Support Assistant
          </h1>
        </div>

        <p className="text-muted-foreground max-w-md">
          An AI-powered voice agent for Quickbite.
          <br />
          Resolve orders, refunds, and delivery issues — instantly.
        </p>

        <Button asChild size="lg" className="rounded-full px-8 mt-2">
          <Link href="/conversation">
            <PhoneCallIcon className="w-4 h-4" />
            Call Support
          </Link>
        </Button>
      </section>
    </main>
  );
}
