import { Header } from "@/components/header"
import { HeroSection } from "@/components/hero-section"
import { TerminalDemo } from "@/components/terminal-demo"
import { FeaturesSection } from "@/components/features-section"
import { InstallationSection } from "@/components/installation-section"
import { UseCasesSection } from "@/components/use-cases-section"
import { Footer } from "@/components/footer"

export default function HomePage() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <Header />
      <HeroSection />
      <TerminalDemo />
      <FeaturesSection />
      <InstallationSection />
      <UseCasesSection />
      <Footer />
    </main>
  )
}
