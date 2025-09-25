import { MessageSquare, Code, Lightbulb, Bug, BookOpen, Rocket } from "lucide-react"

export function UseCasesSection() {
  const useCases = [
    {
      icon: MessageSquare,
      title: "AI Prompt Engineering",
      description: "Perfect context for ChatGPT, Claude, and Gemini conversations",
      example: '"Help me refactor this React component for better performance"',
      ascii: "💬",
    },
    {
      icon: Code,
      title: "Code Reviews",
      description: "Share entire project structure for comprehensive reviews",
      example: '"Review my authentication implementation for security issues"',
      ascii: "👀",
    },
    {
      icon: Lightbulb,
      title: "Architecture Planning",
      description: "Get AI suggestions for project structure and patterns",
      example: '"How can I improve the architecture of this microservice?"',
      ascii: "🏗️",
    },
    {
      icon: Bug,
      title: "Debugging Help",
      description: "Provide full context when asking for debugging assistance",
      example: '"Find the bug causing this authentication error"',
      ascii: "🐛",
    },
    {
      icon: BookOpen,
      title: "Documentation",
      description: "Generate comprehensive documentation from your codebase",
      example: '"Create API documentation for this Express.js project"',
      ascii: "📚",
    },
    {
      icon: Rocket,
      title: "Migration Planning",
      description: "Plan technology migrations with AI assistance",
      example: '"Help me migrate from JavaScript to TypeScript"',
      ascii: "🚀",
    },
  ]

  return (
    <section id="usage" className="py-16 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4 terminal-glow">
            <span className="text-secondary">{">"}</span> Use Cases
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            From debugging to architecture planning, CodePrint bridges the gap between your code and AI-powered
            development workflows.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {useCases.map((useCase, index) => (
            <div
              key={index}
              className="p-6 bg-card border border-border rounded-lg hover:border-primary/50 transition-all duration-300 group"
            >
              <div className="flex items-center gap-3 mb-4">
                <span className="text-2xl">{useCase.ascii}</span>
                <useCase.icon className="w-5 h-5 text-primary group-hover:text-secondary transition-colors" />
              </div>

              <h3 className="text-lg font-semibold mb-2 terminal-glow">{useCase.title}</h3>

              <p className="text-muted-foreground text-sm mb-4 leading-relaxed">{useCase.description}</p>

              <div className="p-3 bg-background border border-border rounded text-xs font-mono">
                <span className="text-muted-foreground">Example:</span>
                <div className="text-primary mt-1">"{useCase.example}"</div>
              </div>
            </div>
          ))}
        </div>

        {/* AI Compatibility */}
        <div className="mt-16 text-center">
          <h3 className="text-xl font-semibold mb-6 terminal-glow">🤖 AI Assistant Compatibility</h3>
          <div className="flex flex-wrap justify-center gap-4">
            {["ChatGPT", "Claude", "Gemini", "GitHub Copilot", "Cursor", "v0"].map((ai, index) => (
              <div key={index} className="px-4 py-2 bg-card border border-primary/30 rounded-lg terminal-border">
                <span className="text-primary terminal-glow">✓</span> {ai}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
