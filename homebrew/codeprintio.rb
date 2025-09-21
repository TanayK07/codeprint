class Codeprintio < Formula
  desc "AI-ready code snapshots for any project"
  homepage "https://github.com/Tanayk07/codeprint"
  url "https://github.com/Tanayk07/codeprint/archive/v1.0.7.tar.gz"
  sha256 "406fb056168004a282c6e328a317f7e6d773e7a93e2e93ec7f1c0b76320b992f"
  license "MIT"
  head "https://github.com/Tanayk07/codeprint.git", branch: "main"

  depends_on "python@3.12"

  resource "colorama" do
    url "https://files.pythonhosted.org/packages/d8/53/6f443c9a4a8358a93a6792e2acffb9d9d5cb0a5cfd8802644b7b1c9a02e4a/colorama-0.4.6.tar.gz"
    sha256 "08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44"
  end

  resource "pyperclip" do
    url "https://files.pythonhosted.org/packages/30/23/2f0a3efc4d6a32f3b63cdff36cd398d9701d26cda58e3ab97ac79fb5e60d/pyperclip-1.9.0.tar.gz"
    sha256 "b7de0142ddc81bfc5c7507eea19da920b92252b548b96186caf94a5e2527d310"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    # Test that the command works
    assert_match "CodePrint", shell_output("#{bin}/codeprint --help")
    
    # Test that it can import properly
    system "#{bin}/codeprint", "--version"
  end
end