"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Play, Pause, RotateCcw } from "lucide-react"

export function TerminalDemo() {
  const [currentStep, setCurrentStep] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentLine, setCurrentLine] = useState(0)

  const terminalSteps = [
    {
      command: "codeprint scan",
      output: [
        "🔍 Scanning project structure...",
        "📁 Detected: React TypeScript Project",
        "⚡ Processing 47 files in parallel...",
        "✅ Generated snapshot in 0.8s",
      ],
    },
    {
      command: "codeprint --format mcp",
      output: [
        "🎯 Generating MCP format...",
        "📋 Optimized for AI assistants",
        "💾 Saved to: project-snapshot.mcp",
        "📊 Size: 15.2KB (compressed from 2.1MB)",
      ],
    },
    {
      command: "codeprint --clipboard",
      output: [
        "📋 Copying to clipboard...",
        "✨ Ready for AI assistant!",
        "🤖 Compatible with: ChatGPT, Claude, Gemini",
        "🎉 Happy prompting!",
      ],
    },
  ]

  useEffect(() => {
    if (isPlaying) {
      const timer = setTimeout(() => {
        if (currentLine < terminalSteps[currentStep].output.length - 1) {
          setCurrentLine(currentLine + 1)
        } else if (currentStep < terminalSteps.length - 1) {
          setCurrentStep(currentStep + 1)
          setCurrentLine(0)
        } else {
          setIsPlaying(false)
        }
      }, 800)
      return () => clearTimeout(timer)
    }
  }, [currentStep, currentLine, isPlaying])

  const startDemo = () => {
    setIsPlaying(true)
    if (currentStep === terminalSteps.length - 1 && currentLine === terminalSteps[currentStep].output.length - 1) {
      setCurrentStep(0)
      setCurrentLine(0)
    }
  }

  const resetDemo = () => {
    setIsPlaying(false)
    setCurrentStep(0)
    setCurrentLine(0)
  }

  return (
    <section id="demo" className="py-16 px-4 bg-card/10">
      <div className="container mx-auto max-w-5xl">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4 terminal-glow">
            <span className="text-secondary">{">"}</span> Live Terminal Demo
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Watch CodePrint transform a real project in seconds with parallel processing
          </p>
        </div>

        <div className="bg-background border-2 border-primary/20 rounded-lg overflow-hidden terminal-border shadow-2xl">
          {/* Terminal Header */}
          <div className="flex items-center justify-between px-4 py-3 bg-card/50 border-b border-border">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-accent"></div>
              <div className="w-3 h-3 rounded-full bg-secondary"></div>
              <div className="w-3 h-3 rounded-full bg-primary"></div>
            </div>
            <span className="text-sm text-muted-foreground font-mono">terminal — codeprint demo</span>
            <div className="w-16"></div>
          </div>

          {/* Terminal Content */}
          <div className="p-6 space-y-4 min-h-[350px] font-mono text-sm">
            {terminalSteps.slice(0, currentStep + 1).map((step, stepIndex) => (
              <div key={stepIndex} className="space-y-2">
                <div className="text-primary flex items-center">
                  <span className="text-secondary">user@codeprint:~$</span>
                  <span className="ml-2">{step.command}</span>
                </div>
                <div className="space-y-1 ml-6">
                  {step.output
                    .slice(0, stepIndex === currentStep ? currentLine + 1 : step.output.length)
                    .map((line, lineIndex) => (
                      <div key={lineIndex} className="text-muted-foreground animate-in fade-in duration-300">
                        {line}
                      </div>
                    ))}
                </div>
              </div>
            ))}

            {/* Cursor */}
            <div className="flex items-center">
              <span className="text-secondary">user@codeprint:~$</span>
              <span className="ml-2 w-2 h-5 bg-primary animate-pulse"></span>
            </div>
          </div>

          {/* Controls */}
          <div className="flex justify-center gap-3 px-6 py-4 bg-card/30 border-t border-border">
            <Button onClick={startDemo} disabled={isPlaying} className="terminal-glow">
              {isPlaying ? (
                <>
                  <Pause className="w-4 h-4 mr-2" />
                  Running...
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 mr-2" />
                  Run Demo
                </>
              )}
            </Button>
            <Button variant="outline" onClick={resetDemo} disabled={isPlaying}>
              <RotateCcw className="w-4 h-4 mr-2" />
              Reset
            </Button>
          </div>
        </div>

        {/* Before/After Comparison */}
        <div className="mt-12 grid md:grid-cols-2 gap-6">
          <div className="p-6 bg-card border border-border rounded-lg">
            <h3 className="text-lg font-semibold mb-4 text-accent">❌ Before CodePrint</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>• Manually copying files one by one</li>
              <li>• Overwhelming AI with too much context</li>
              <li>• Missing important dependencies</li>
              <li>• Inconsistent formatting</li>
              <li>• Time-consuming setup</li>
            </ul>
          </div>

          <div className="p-6 bg-card border border-primary/30 rounded-lg terminal-border">
            <h3 className="text-lg font-semibold mb-4 text-primary terminal-glow">✅ After CodePrint</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>• One command, entire project captured</li>
              <li>• Optimized for AI token limits</li>
              <li>• Smart dependency detection</li>
              <li>• Beautiful, consistent formatting</li>
              <li>• Lightning-fast parallel processing</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  )
}
