"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Copy, Check, Package } from "lucide-react"

export function InstallationSection() {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null)

  const installMethods = [
    {
      name: "npm",
      command: "npm install -g codeprintio",
      description: "Node.js package manager",
      icon: "📦",
      url: "https://www.npmjs.com/package/codeprintio",
    },
    {
      name: "PyPI",
      command: "pip install codeprintio",
      description: "Python package index",
      icon: "🐍",
      url: "https://pypi.org/project/codeprintio/",
    },
    {
      name: "GitHub",
      command: "git clone https://github.com/Tanayk07/codeprint",
      description: "Build from source",
      icon: "🔧",
      url: "https://github.com/Tanayk07/codeprint",
    },
    {
      name: "Chocolatey",
      command: "choco install codeprint",
      description: "Coming soon for Windows",
      icon: "🍫",
      disabled: true,
    },
  ]

  const copyToClipboard = async (text: string, index: number) => {
    await navigator.clipboard.writeText(text)
    setCopiedIndex(index)
    setTimeout(() => setCopiedIndex(null), 2000)
  }

  return (
    <section id="install" className="py-16 px-4 bg-card/10">
      <div className="container mx-auto max-w-4xl">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4 terminal-glow">
            <span className="text-secondary">{">"}</span> Installation
          </h2>
          <p className="text-muted-foreground">Choose your preferred installation method and get started in seconds</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {installMethods.map((method, index) => (
            <div
              key={index}
              className={`p-6 bg-card border rounded-lg transition-all duration-300 ${
                method.disabled ? "border-border opacity-50" : "border-border hover:border-primary/50 terminal-border"
              }`}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{method.icon}</span>
                  <div>
                    <h3 className="font-semibold terminal-glow">{method.name}</h3>
                    <p className="text-sm text-muted-foreground">{method.description}</p>
                  </div>
                </div>
                {method.url && (
                  <Button variant="ghost" size="sm" asChild>
                    <a href={method.url} target="_blank" rel="noopener noreferrer">
                      <Package className="w-4 h-4" />
                    </a>
                  </Button>
                )}
              </div>

              <div className="bg-background border border-border rounded p-3 font-mono text-sm">
                <div className="flex items-center justify-between">
                  <code className="text-primary">
                    <span className="text-secondary">$</span> {method.command}
                  </code>
                  {!method.disabled && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => copyToClipboard(method.command, index)}
                      className="ml-2"
                    >
                      {copiedIndex === index ? (
                        <Check className="w-4 h-4 text-primary" />
                      ) : (
                        <Copy className="w-4 h-4" />
                      )}
                    </Button>
                  )}
                </div>
              </div>

              {method.disabled && <div className="mt-3 text-xs text-muted-foreground text-center">Coming Soon</div>}
            </div>
          ))}
        </div>

        {/* Quick Start */}
        <div className="mt-12 p-6 bg-card border border-primary/30 rounded-lg terminal-border">
          <h3 className="text-lg font-semibold mb-4 terminal-glow">🚀 Quick Start</h3>
          <div className="space-y-3 font-mono text-sm">
            <div className="flex items-center gap-2">
              <span className="text-secondary">1.</span>
              <code className="text-primary">npm install -g codeprintio</code>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-secondary">2.</span>
              <code className="text-primary">cd your-project</code>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-secondary">3.</span>
              <code className="text-primary">codeprint scan</code>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-secondary">4.</span>
              <span className="text-muted-foreground">Share with your AI assistant! 🎉</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
