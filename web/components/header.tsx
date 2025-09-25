"use client"

import { Button } from "@/components/ui/button"
import { Terminal, Menu, X, BookOpen, Star } from "lucide-react"
import { useState, useEffect } from "react"

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [starCount, setStarCount] = useState<number | null>(null)

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

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: "smooth" })
    }
  }

  return (
    <header className="border-b-2 border-border bg-background sticky top-0 z-50 retro-shadow">
      <div className="container mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary text-primary-foreground retro-border">
              <Terminal className="w-6 h-6" />
            </div>
            <div>
              <span className="text-2xl font-bold retro-text-shadow">CodePrint</span>
              <div className="text-xs text-muted-foreground font-mono">v2.1.0</div>
            </div>
          </div>
        </div>

        <nav className="hidden lg:flex items-center gap-8">
          <button
            onClick={() => scrollToSection("features")}
            className="text-sm font-medium text-foreground hover:text-primary transition-colors focus-visible-ring px-3 py-2 rounded"
          >
            Features
          </button>
          <button
            onClick={() => scrollToSection("demo")}
            className="text-sm font-medium text-foreground hover:text-primary transition-colors focus-visible-ring px-3 py-2 rounded"
          >
            Live Demo
          </button>
          <button
            onClick={() => scrollToSection("install")}
            className="text-sm font-medium text-foreground hover:text-primary transition-colors focus-visible-ring px-3 py-2 rounded"
          >
            Installation
          </button>
          <button
            onClick={() => scrollToSection("usage")}
            className="text-sm font-medium text-foreground hover:text-primary transition-colors focus-visible-ring px-3 py-2 rounded"
          >
            Use Cases
          </button>
          <a
            href="/docs"
            className="text-sm font-medium text-foreground hover:text-primary transition-colors focus-visible-ring px-3 py-2 rounded"
          >
            Docs
          </a>
        </nav>

        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" asChild className="hidden sm:flex retro-border hover-lift bg-transparent">
            <a href="https://github.com/TanayK07/codeprint" target="_blank" rel="noopener noreferrer">
              <Star className="w-4 h-4 mr-2 text-yellow-500 fill-yellow-500" />
              <span className="hidden md:inline">Star</span>
              {starCount && <span className="ml-1 bg-muted px-2 py-1 rounded text-xs">{starCount}</span>}
            </a>
          </Button>
          <Button size="sm" className="retro-border retro-shadow hover-lift bg-primary text-primary-foreground">
            Get Started
          </Button>

          {/* Mobile menu button */}
          <Button
            variant="ghost"
            size="sm"
            className="lg:hidden focus-visible-ring"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </Button>
        </div>
      </div>

      {mobileMenuOpen && (
        <div className="lg:hidden border-t-2 border-border bg-muted">
          <nav className="container mx-auto px-6 py-6 space-y-4">
            <button
              onClick={() => {
                scrollToSection("features")
                setMobileMenuOpen(false)
              }}
              className="block text-sm font-medium text-foreground hover:text-primary transition-colors focus-visible-ring px-3 py-2 rounded w-full text-left"
            >
              Features
            </button>
            <button
              onClick={() => {
                scrollToSection("demo")
                setMobileMenuOpen(false)
              }}
              className="block text-sm font-medium text-foreground hover:text-primary transition-colors focus-visible-ring px-3 py-2 rounded w-full text-left"
            >
              Live Demo
            </button>
            <button
              onClick={() => {
                scrollToSection("install")
                setMobileMenuOpen(false)
              }}
              className="block text-sm font-medium text-foreground hover:text-primary transition-colors focus-visible-ring px-3 py-2 rounded w-full text-left"
            >
              Installation
            </button>
            <button
              onClick={() => {
                scrollToSection("usage")
                setMobileMenuOpen(false)
              }}
              className="block text-sm font-medium text-foreground hover:text-primary transition-colors focus-visible-ring px-3 py-2 rounded w-full text-left"
            >
              Use Cases
            </button>
            <a
              href="/docs"
              className="block text-sm font-medium text-foreground hover:text-primary transition-colors focus-visible-ring px-3 py-2 rounded"
            >
              <BookOpen className="w-4 h-4 inline mr-2" />
              Docs
            </a>
          </nav>
        </div>
      )}
    </header>
  )
}
