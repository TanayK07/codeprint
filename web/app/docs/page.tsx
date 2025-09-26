import { Button } from "@/components/ui/button"
import { ArrowLeft, Terminal, Code, Settings, Zap, FileText } from "lucide-react"
import Link from "next/link"

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b-2 border-border bg-background sticky top-0 z-50 retro-shadow">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="outline" size="sm" asChild className="retro-border hover-lift bg-transparent">
              <Link href="/">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Home
              </Link>
            </Button>
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary text-primary-foreground retro-border">
                <Terminal className="w-5 h-5" />
              </div>
              <div>
                <span className="text-xl font-bold retro-text-shadow">CodePrint Docs</span>
                <div className="text-xs text-muted-foreground font-mono">v2.1.0</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-12 max-w-4xl">
        {/* Basic Usage Section */}
        <section className="mb-16">
          <div className="flex items-center gap-3 mb-8">
            <Code className="w-6 h-6 text-primary" />
            <h1 className="text-3xl font-bold retro-text-shadow">Basic Usage</h1>
          </div>

          <div className="space-y-6">
            <div className="bg-card border-2 border-border retro-border retro-shadow p-6">
              <h3 className="text-lg font-bold mb-4">Scan current directory and save to file:</h3>
              <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                <code className="text-primary font-mono block">
                  <span className="text-secondary">$</span> codeprint
                </code>
              </div>
            </div>

            <div className="bg-card border-2 border-border retro-border retro-shadow p-6">
              <h3 className="text-lg font-bold mb-4">Scan with specific format:</h3>
              <div className="space-y-3">
                <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                  <code className="text-primary font-mono block">
                    <span className="text-secondary">$</span> codeprint -f mcp{" "}
                    <span className="text-muted-foreground"># Generate MCP format</span>
                  </code>
                </div>
                <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                  <code className="text-primary font-mono block">
                    <span className="text-secondary">$</span> codeprint -f txt{" "}
                    <span className="text-muted-foreground"># Generate TXT format (default)</span>
                  </code>
                </div>
              </div>
            </div>

            <div className="bg-card border-2 border-border retro-border retro-shadow p-6">
              <h3 className="text-lg font-bold mb-4">Copy to clipboard automatically:</h3>
              <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                <code className="text-primary font-mono block">
                  <span className="text-secondary">$</span> codeprint -c
                </code>
              </div>
            </div>
          </div>
        </section>

        {/* Advanced Usage Section */}
        <section className="mb-16">
          <div className="flex items-center gap-3 mb-8">
            <Settings className="w-6 h-6 text-primary" />
            <h2 className="text-3xl font-bold retro-text-shadow">Advanced Usage</h2>
          </div>

          <div className="grid gap-6">
            <div className="bg-card border-2 border-border retro-border retro-shadow p-6">
              <div className="space-y-4">
                <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                  <code className="text-primary font-mono block mb-2">
                    <span className="text-secondary">$</span> codeprint -p /path/to/project
                  </code>
                  <p className="text-sm text-muted-foreground">Scan specific directory</p>
                </div>

                <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                  <code className="text-primary font-mono block mb-2">
                    <span className="text-secondary">$</span> codeprint -o my_snapshot.txt
                  </code>
                  <p className="text-sm text-muted-foreground">Custom output file</p>
                </div>

                <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                  <code className="text-primary font-mono block mb-2">
                    <span className="text-secondary">$</span> codeprint --include-hidden
                  </code>
                  <p className="text-sm text-muted-foreground">Include hidden files</p>
                </div>

                <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                  <code className="text-primary font-mono block mb-2">
                    <span className="text-secondary">$</span> codeprint --max-files 1000 --max-file-size 2048
                    --max-lines 2000
                  </code>
                  <p className="text-sm text-muted-foreground">Set custom limits</p>
                </div>

                <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                  <code className="text-primary font-mono block mb-2">
                    <span className="text-secondary">$</span> codeprint --no-auto-detect
                  </code>
                  <p className="text-sm text-muted-foreground">Disable automatic project detection</p>
                </div>

                <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                  <code className="text-primary font-mono block mb-2">
                    <span className="text-secondary">$</span> codeprint --no-gitignore
                  </code>
                  <p className="text-sm text-muted-foreground">Disable gitignore patterns</p>
                </div>

                <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                  <code className="text-primary font-mono block mb-2">
                    <span className="text-secondary">$</span> codeprint -v
                  </code>
                  <p className="text-sm text-muted-foreground">Verbose output</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Project Type Detection Section */}
        <section className="mb-16">
          <div className="flex items-center gap-3 mb-8">
            <Zap className="w-6 h-6 text-primary" />
            <h2 className="text-3xl font-bold retro-text-shadow">🎯 Project Type Detection</h2>
          </div>

          <div className="bg-card border-2 border-border retro-border retro-shadow p-6">
            <p className="text-base text-muted-foreground mb-6">
              CodePrint automatically detects your project type and applies appropriate ignore patterns:
            </p>

            <div className="overflow-x-auto">
              <table className="w-full border-2 border-border">
                <thead>
                  <tr className="bg-muted border-b-2 border-border">
                    <th className="text-left p-4 font-bold">Project Type</th>
                    <th className="text-left p-4 font-bold">Detection Files</th>
                    <th className="text-left p-4 font-bold">Auto-Ignored</th>
                  </tr>
                </thead>
                <tbody className="font-mono text-sm">
                  <tr className="border-b border-border">
                    <td className="p-4 font-bold">Python</td>
                    <td className="p-4">requirements.txt, setup.py, pyproject.toml</td>
                    <td className="p-4">__pycache__, *.pyc, venv/, .egg-info/</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="p-4 font-bold">JavaScript</td>
                    <td className="p-4">package.json</td>
                    <td className="p-4">node_modules/, dist/, *.min.js</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="p-4 font-bold">TypeScript</td>
                    <td className="p-4">tsconfig.json</td>
                    <td className="p-4">node_modules/, dist/, *.d.ts</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="p-4 font-bold">Java</td>
                    <td className="p-4">pom.xml, build.gradle</td>
                    <td className="p-4">target/, *.class, .gradle/</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="p-4 font-bold">Android</td>
                    <td className="p-4">AndroidManifest.xml, gradle.properties</td>
                    <td className="p-4">build/, *.apk, *.aab</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="p-4 font-bold">iOS</td>
                    <td className="p-4">Podfile, *.xcodeproj</td>
                    <td className="p-4">Pods/, *.ipa, DerivedData/</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="p-4 font-bold">React</td>
                    <td className="p-4">package.json + React files</td>
                    <td className="p-4">node_modules/, build/, .next/</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="p-4 font-bold">.NET</td>
                    <td className="p-4">*.csproj, *.sln</td>
                    <td className="p-4">bin/, obj/, packages/</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="p-4 font-bold">Go</td>
                    <td className="p-4">go.mod</td>
                    <td className="p-4">vendor/, *.exe</td>
                  </tr>
                  <tr className="border-b border-border">
                    <td className="p-4 font-bold">Rust</td>
                    <td className="p-4">Cargo.toml</td>
                    <td className="p-4">target/, Cargo.lock</td>
                  </tr>
                  <tr>
                    <td className="p-4 font-bold">Flutter</td>
                    <td className="p-4">pubspec.yaml</td>
                    <td className="p-4">build/, .dart_tool/</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* Output Formats Section */}
        <section className="mb-16">
          <div className="flex items-center gap-3 mb-8">
            <FileText className="w-6 h-6 text-primary" />
            <h2 className="text-3xl font-bold retro-text-shadow">📋 Output Formats</h2>
          </div>

          <div className="grid gap-6">
            <div className="bg-card border-2 border-border retro-border retro-shadow p-6">
              <h3 className="text-xl font-bold mb-4">TXT Format</h3>
              <p className="text-muted-foreground mb-4">
                Simple text format with file contents and directory structure. Perfect for quick sharing.
              </p>
            </div>

            <div className="bg-card border-2 border-border retro-border retro-shadow p-6">
              <h3 className="text-xl font-bold mb-4">MCP Format (Markdown Context Pack)</h3>
              <p className="text-muted-foreground mb-4">
                Structured markdown format with metadata, syntax highlighting, and better organization. Ideal for AI
                assistants.
              </p>
            </div>
          </div>
        </section>

        {/* Configuration Section */}
        <section className="mb-16">
          <div className="flex items-center gap-3 mb-8">
            <Settings className="w-6 h-6 text-primary" />
            <h2 className="text-3xl font-bold retro-text-shadow">⚙️ Configuration</h2>
          </div>

          <div className="space-y-8">
            <div className="bg-card border-2 border-border retro-border retro-shadow p-6">
              <h3 className="text-xl font-bold mb-6">Command-Line Flags</h3>
              <div className="overflow-x-auto">
                <table className="w-full border-2 border-border">
                  <thead>
                    <tr className="bg-muted border-b-2 border-border">
                      <th className="text-left p-4 font-bold">Flag</th>
                      <th className="text-left p-4 font-bold">Description</th>
                      <th className="text-left p-4 font-bold">Default</th>
                    </tr>
                  </thead>
                  <tbody className="font-mono text-sm">
                    <tr className="border-b border-border">
                      <td className="p-4">-f, --format</td>
                      <td className="p-4">Output format (txt/mcp)</td>
                      <td className="p-4">txt</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-4">-o, --output</td>
                      <td className="p-4">Output file name</td>
                      <td className="p-4">auto-generated</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-4">-c, --clipboard</td>
                      <td className="p-4">Copy to clipboard</td>
                      <td className="p-4">false</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-4">-p, --path</td>
                      <td className="p-4">Path to scan</td>
                      <td className="p-4">current directory</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-4">--max-file-size</td>
                      <td className="p-4">Max file size (KB)</td>
                      <td className="p-4">1024</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-4">--max-files</td>
                      <td className="p-4">Max number of files</td>
                      <td className="p-4">500</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-4">--max-lines</td>
                      <td className="p-4">Max lines per file</td>
                      <td className="p-4">1000</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-4">--include-hidden</td>
                      <td className="p-4">Include hidden files</td>
                      <td className="p-4">false</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-4">--no-gitignore</td>
                      <td className="p-4">Ignore .gitignore patterns</td>
                      <td className="p-4">false</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-4">--no-auto-detect</td>
                      <td className="p-4">Disable project type detection</td>
                      <td className="p-4">false</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-4">--no-progress</td>
                      <td className="p-4">Disable progress output</td>
                      <td className="p-4">false</td>
                    </tr>
                    <tr className="border-b border-border">
                      <td className="p-4">--no-parallel</td>
                      <td className="p-4">Disable parallel processing</td>
                      <td className="p-4">false</td>
                    </tr>
                    <tr>
                      <td className="p-4">-v, --verbose</td>
                      <td className="p-4">Verbose output</td>
                      <td className="p-4">false</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div className="bg-card border-2 border-border retro-border retro-shadow p-6">
              <h3 className="text-xl font-bold mb-4">Environment Variables</h3>
              <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                <code className="text-primary font-mono block space-y-2">
                  <div>export GEMINI_DEFAULT_FORMAT=mcp</div>
                  <div>export GEMINI_CLIPBOARD=true</div>
                  <div>export GEMINI_MAX_FILES=1000</div>
                </code>
              </div>
            </div>
          </div>
        </section>

        {/* Development Section */}
        <section className="mb-16">
          <div className="flex items-center gap-3 mb-8">
            <Code className="w-6 h-6 text-primary" />
            <h2 className="text-3xl font-bold retro-text-shadow">🔧 Development</h2>
          </div>

          <div className="bg-card border-2 border-border retro-border retro-shadow p-6">
            <h3 className="text-xl font-bold mb-6">Building from Source</h3>
            <div className="space-y-4">
              <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                <code className="text-primary font-mono block space-y-2">
                  <div>
                    <span className="text-muted-foreground"># Clone the repository</span>
                  </div>
                  <div>
                    <span className="text-secondary">$</span> git clone https://github.com/Tanayk07/codeprint.git
                  </div>
                  <div>
                    <span className="text-secondary">$</span> cd codeprint
                  </div>
                </code>
              </div>

              <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                <code className="text-primary font-mono block space-y-2">
                  <div>
                    <span className="text-muted-foreground"># Install dependencies</span>
                  </div>
                  <div>
                    <span className="text-secondary">$</span> pip install -r requirements.txt
                  </div>
                </code>
              </div>

              <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                <code className="text-primary font-mono block space-y-2">
                  <div>
                    <span className="text-muted-foreground"># Run locally</span>
                  </div>
                  <div>
                    <span className="text-secondary">$</span> python src/codeprint.py
                  </div>
                </code>
              </div>

              <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                <code className="text-primary font-mono block space-y-2">
                  <div>
                    <span className="text-muted-foreground"># Run tests</span>
                  </div>
                  <div>
                    <span className="text-secondary">$</span> pytest tests/
                  </div>
                </code>
              </div>

              <div className="bg-muted border-2 border-border retro-inset rounded p-4">
                <code className="text-primary font-mono block space-y-2">
                  <div>
                    <span className="text-muted-foreground"># Build distributions</span>
                  </div>
                  <div>
                    <span className="text-secondary">$</span> python setup.py sdist bdist_wheel
                  </div>
                </code>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}
