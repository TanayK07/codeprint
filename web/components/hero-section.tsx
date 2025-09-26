"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Copy, ArrowRight, CheckCircle, Sparkles, Code, FileText, Star } from "lucide-react"

export function HeroSection() {
  const [typedText, setTypedText] = useState("")
  const [copied, setCopied] = useState(false)
  const [starCount, setStarCount] = useState<number | null>(null)
  const [isVibrating, setIsVibrating] = useState(false)
  const titleRef = useRef<HTMLDivElement>(null)
  const fullText = "Transform any codebase into AI-ready snapshots"

  useEffect(() => {
    let i = 0
    const timer = setInterval(() => {
      if (i < fullText.length) {
        setTypedText(fullText.slice(0, i + 1))
        i++
      } else {
        clearInterval(timer)
      }
    }, 80)

    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    const fetchStarCount = async () => {
      try {
        const response = await fetch("https://api.github.com/repos/TanayK07/codeprint")
        const data = await response.json()
        setStarCount(data.stargazers_count)
      } catch (error) {
        console.error("Failed to fetch star count:", error)
      }
    }
    fetchStarCount()
  }, [])

  const copyToClipboard = async (text: string) => {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: "smooth" })
    }
  }

  const handleTitleClick = (e: React.MouseEvent) => {
    // Create ripple effect
    const ripple = document.createElement('div')
    ripple.className = 'ripple'
    const rect = e.currentTarget.getBoundingClientRect()
    ripple.style.left = `${e.clientX - rect.left}px`
    ripple.style.top = `${e.clientY - rect.top}px`
    e.currentTarget.querySelector('.ripple-container')?.appendChild(ripple)
    
    // Trigger vibration
    setIsVibrating(true)
    setTimeout(() => setIsVibrating(false), 500)
    
    // Remove ripple after animation
    setTimeout(() => ripple.remove(), 1000)
  }

  return (
    <section className="py-20 md:py-32 px-6 text-center relative overflow-hidden">
      <div className="absolute inset-0 retro-grid opacity-30"></div>

      <div className="container mx-auto max-w-6xl relative">
        <div className="mb-12">
          <div className="inline-flex items-center gap-3 px-4 py-2 bg-card border-2 border-primary retro-border retro-shadow mb-8">
            <div className="w-3 h-3 bg-primary rounded-full pulse-scale"></div>
            <span className="text-sm font-medium">Now with parallel processing & MCP format support</span>
          </div>

          <div className="mb-8">
            {/* Ultra cool animated title with multiple effects */}
            <div 
              className={`relative inline-block group cursor-pointer ${isVibrating ? 'vibrating' : ''}`}
              onClick={handleTitleClick}
              ref={titleRef}
            >
              {/* Background glow effect */}
              <div className="absolute inset-0 blur-3xl opacity-30">
                <div className="absolute inset-0 bg-gradient-to-r from-primary via-secondary to-primary animate-pulse"></div>
              </div>
              
              {/* Main title with cyber effect */}
              <h1 className="relative">
                <div className="text-6xl md:text-8xl lg:text-9xl font-black tracking-tighter">
                  {/* Animated gradient text */}
                  <span className="cyber-text inline-block transition-all duration-300 hover:scale-110" data-text="CODE">
                    CODE
                    <span className="matrix-container absolute inset-0 pointer-events-none opacity-0 group-hover:opacity-100">
                      <span className="matrix-char">0</span>
                      <span className="matrix-char">1</span>
                      <span className="matrix-char">0</span>
                      <span className="matrix-char">1</span>
                      <span className="matrix-char">1</span>
                      <span className="matrix-char">0</span>
                      <span className="matrix-char">1</span>
                      <span className="matrix-char">0</span>
                    </span>
                  </span>
                  <span className="neon-text inline-block ml-2 md:ml-4 transition-all duration-300 hover:scale-110" data-text="PRINT">
                    PRINT
                    <span className="explosion-container absolute inset-0 pointer-events-none">
                      <span className="explosion-particle"></span>
                      <span className="explosion-particle"></span>
                      <span className="explosion-particle"></span>
                      <span className="explosion-particle"></span>
                      <span className="explosion-particle"></span>
                      <span className="explosion-particle"></span>
                    </span>
                  </span>
                </div>
              </h1>

              {/* Animated underline effect */}
              <div className="mt-4 flex items-center justify-center gap-2">
                <div className="scanner-line"></div>
              </div>

              {/* Floating particles */}
              <div className="absolute inset-0 pointer-events-none">
                <div className="particle particle-1"></div>
                <div className="particle particle-2"></div>
                <div className="particle particle-3"></div>
                <div className="particle particle-4"></div>
              </div>

              {/* Click ripple effect container */}
              <div className="ripple-container absolute inset-0 pointer-events-none"></div>
            </div>
          </div>

          <div className="text-lg md:text-xl lg:text-2xl text-muted-foreground mb-8 min-h-[3rem] flex items-center justify-center">
            <span className="typewriter font-mono">{typedText}</span>
          </div>
        </div>

        <p className="text-base md:text-lg text-muted-foreground mb-12 max-w-4xl mx-auto leading-relaxed">
          Lightning-fast CLI tool that creates clean, AI-optimized code snapshots. Perfect for{" "}
          <span className="text-primary font-bold bg-muted px-2 py-1 rounded">ChatGPT</span>,{" "}
          <span className="text-primary font-bold bg-muted px-2 py-1 rounded">Claude</span>, and{" "}
          <span className="text-primary font-bold bg-muted px-2 py-1 rounded">Gemini</span>.
        </p>

        <div className="mb-12 max-w-3xl mx-auto">
          <div className="bg-card border-2 border-border retro-border retro-shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Code className="w-4 h-4 text-primary" />
                <span className="text-base font-bold">Quick Install</span>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => copyToClipboard("npm install -g codeprintio")}
                className="retro-border hover-lift"
              >
                {copied ? (
                  <>
                    <CheckCircle className="w-4 h-4 mr-2 text-primary" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="w-4 h-4 mr-2" />
                    Copy
                  </>
                )}
              </Button>
            </div>
            <div className="bg-muted border-2 border-border retro-inset rounded p-4">
              <code className="text-primary text-lg font-mono block">
                <span className="text-secondary">$</span> npm install -g codeprintio
              </code>
            </div>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
          <Button
            size="lg"
            className="retro-border retro-shadow hover-lift bg-primary text-primary-foreground px-8 py-3 text-base font-bold"
          >
            <Sparkles className="w-4 h-4 mr-2" />
            Get Started Now
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
          <Button
            variant="outline"
            size="lg"
            className="retro-border hover-lift px-8 py-3 text-base font-medium bg-transparent"
            onClick={() => scrollToSection("demo")}
          >
            <FileText className="w-4 h-4 mr-2" />
            View Live Demo
          </Button>
          <Button
            variant="outline"
            size="lg"
            className="retro-border hover-lift px-8 py-3 text-base font-medium bg-transparent"
            asChild
          >
            <a href="https://github.com/TanayK07/codeprint" target="_blank" rel="noopener noreferrer">
              <Star className="w-4 h-4 mr-2 text-yellow-500 fill-yellow-500" />
              Star on GitHub
              {starCount && <span className="ml-2 bg-muted px-2 py-1 rounded text-sm">{starCount}</span>}
            </a>
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="group p-8 bg-card border-2 border-border retro-border retro-shadow hover-lift transition-all duration-300">
            <div className="text-5xl font-bold text-primary retro-text-shadow mb-4 group-hover:pulse-scale">10x</div>
            <div className="text-lg font-bold text-foreground mb-2">Faster Processing</div>
            <div className="text-sm text-muted-foreground">Parallel file processing with optimized algorithms</div>
          </div>
          <div className="group p-8 bg-card border-2 border-border retro-border retro-shadow hover-lift transition-all duration-300">
            <div className="text-5xl font-bold text-secondary retro-text-shadow mb-4 group-hover:pulse-scale">50+</div>
            <div className="text-lg font-bold text-foreground mb-2">Project Types</div>
            <div className="text-sm text-muted-foreground">Universal compatibility across all frameworks</div>
          </div>
          <div className="group p-8 bg-card border-2 border-border retro-border retro-shadow hover-lift transition-all duration-300">
            <div className="text-5xl font-bold text-accent retro-text-shadow mb-4 group-hover:pulse-scale">100%</div>
            <div className="text-lg font-bold text-foreground mb-2">AI Compatible</div>
            <div className="text-sm text-muted-foreground">Optimized output format for all major LLMs</div>
          </div>
        </div>
      </div>
    </section>
  )
}