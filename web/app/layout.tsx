import type React from "react"
import type { Metadata } from "next"
import { JetBrains_Mono } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import { Suspense } from "react"
import "./globals.css"

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
  display: "swap",
})

export const metadata: Metadata = {
  title: "CodePrint - AI-Ready Code Snapshots",
  description:
    "Lightning-fast CLI tool that creates beautiful, AI-ready code snapshots for any project. Perfect for ChatGPT, Claude, and Gemini.",
  keywords: ["code snapshot", "AI tools", "prompt engineering", "CLI", "developer tools"],
  authors: [{ name: "CodePrint Team" }],
  openGraph: {
    title: "CodePrint - AI-Ready Code Snapshots",
    description: "Lightning-fast CLI tool that creates beautiful, AI-ready code snapshots for any project.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "CodePrint - AI-Ready Code Snapshots",
    description: "Lightning-fast CLI tool that creates beautiful, AI-ready code snapshots for any project.",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`font-mono ${jetbrainsMono.variable} scanlines crt-flicker`}>
        <Suspense fallback={<div>Loading...</div>}>{children}</Suspense>
        <Analytics />
      </body>
    </html>
  )
}
