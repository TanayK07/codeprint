import { Zap, Brain, Cpu, Copy, Shield, Globe } from "lucide-react"

export function FeaturesSection() {
  const features = [
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Parallel processing scans thousands of files in seconds",
      ascii: "⚡",
    },
    {
      icon: Brain,
      title: "AI Optimized",
      description: "Perfect formatting for ChatGPT, Claude, and Gemini",
      ascii: "🤖",
    },
    {
      icon: Cpu,
      title: "Smart Detection",
      description: "Automatically detects project type and structure",
      ascii: "🎯",
    },
    {
      icon: Copy,
      title: "Instant Clipboard",
      description: "One-click copy to share with AI assistants",
      ascii: "📋",
    },
    {
      icon: Shield,
      title: "Multiple Formats",
      description: "TXT, MCP, and custom output formats",
      ascii: "📄",
    },
    {
      icon: Globe,
      title: "Cross Platform",
      description: "Works on Windows, macOS, and Linux",
      ascii: "🌍",
    },
  ]

  return (
    <section id="features" className="py-16 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4 terminal-glow">
            <span className="text-secondary">{">"}</span> Features
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Built for the AI era of development. Every feature designed to bridge the gap between your code and AI
            assistants.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div
              key={index}
              className="p-6 bg-card border border-border rounded-lg hover:border-primary/50 transition-all duration-300 group"
            >
              <div className="flex items-center gap-4 mb-4">
                <div className="text-2xl">{feature.ascii}</div>
                <feature.icon className="w-6 h-6 text-primary group-hover:text-secondary transition-colors" />
              </div>
              <h3 className="text-lg font-semibold mb-2 terminal-glow">{feature.title}</h3>
              <p className="text-muted-foreground text-sm leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>

        {/* ASCII Art Divider */}
        <div className="mt-16 text-center text-primary/30 font-mono text-xs">
          <pre>
            {`
════════════════════════════════════════════════════════════════════════════════
`}
          </pre>
        </div>
      </div>
    </section>
  )
}
