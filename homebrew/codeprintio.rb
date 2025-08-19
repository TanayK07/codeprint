class Codeprintio < Formula
  desc "A powerful cross-platform tool for creating AI-ready project snapshots"
  homepage "https://github.com/Tanayk07/codeprint"
  url "https://github.com/Tanayk07/codeprint/archive/v1.0.3.tar.gz"
  sha256 "YOUR_SHA256_HERE"
  license "MIT"

  depends_on "python@3.9"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/codeprint", "--version"
  end
end
