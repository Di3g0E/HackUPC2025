{ pkgs, lib, config, inputs, ... }:

{

  # https://devenv.sh/packages/
  packages = with pkgs; [
    ruff
    python312Packages.jedi-language-server
    python312Packages.python-lsp-server
  ];

  languages.python = {
    enable = true;
    uv = {
      enable = true;
      sync.enable = true;
    };
  };

}
